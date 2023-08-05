#!/usr/bin/env python3
import argparse
import collections
import functools
import itertools
import logging
import os
import random
import signal
import sys
import threading
import time
import uuid

from proton.handlers import MessagingHandler
from proton.reactor import ApplicationEvent
from proton.reactor import Container
from proton.reactor import Delivery
from proton.reactor import EventInjector
from proton import Disposition
import proton

from .base import Router


parser = argparse.ArgumentParser(
    prog='aorta publisher',
    description="Route incoming messages to the Aorta messaging infrastructure.")
parser.add_argument('-U', dest='peers', default=[], action='append',
    help="specifies the upstream AMQP peers by ip:port.")
parser.add_argument('--loglevel', default=os.environ.get('AORTA_LOGLEVEL','INFO'),
    choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'],
    help="specifies the logging verbosity (default: %(default)s)")
parser.add_argument('--ingress-channel', default='aorta.ingress',
    help="the ingress message channel at the AMQP peer (default: %(default)s)")
parser.add_argument('--routes', dest='routes', default=[], action='append',
    help="specifices additional routes configuration files.")


class MessageRouter(MessagingHandler):
    """Accepts incoming messages and routes them to the configured
    destinations.

    The :class:`MessageRouter` informs the AMQP peer that a message is
    accepted when it is written to disk or accepted by the upstream AMQP
    peer.

    If a message does not conform to the Aorta protocol, it is rejected
    by :class:`MessageRouter` and this is its ultimate state. Clients
    must not retransmit the message.

    :class:`MessageRouter` does not accept clients trying to create
    receiving links (a :class:`proton.Sender` instance from our
    perspective). Should a client attempt to do so, it is dropped
    with an error condition. The only :class:`proton.Sender` instances
    allowed to exist, are the links to the upstream AMQP peers.
    """
    framerate = 20

    @property
    def sendables(self):
        # TODO: Also check if the links are actually established
        # and alives.
        return [x for x in self.senders if x.credit]

    @property
    def routes(self):
        """Return all possible routes currently configured."""
        return self.router.get_possible_routes()

    def __init__(self, remotes, channel, routes=None, buf=None, loglevel='INFO'):
        """Initialize a new :class:`MessagePublisher` instance."""
        super(MessageRouter, self).__init__(
            auto_settle=False, auto_accept=False)

        # Conigure the logger to send everything to stdout. We use
        # the default IBR logging pattern.
        self.loglevel = getattr(logging, loglevel)
        self.logger = logging.getLogger('aorta.router')
        self.loghandler = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter(
            "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            datefmt="[%Y-%m-%d %H:%M:%S %z]")
        self.loghandler.setFormatter(fmt)
        self.logger.addHandler(self.loghandler)
        self.loghandler.setLevel(self.loglevel)
        self.logger.setLevel(self.loglevel)

        self.ingress = collections.defaultdict(list)
        self.egress = {}
        self.remotes = remotes
        self.router = Router()
        self.channel = channel
        self.senders = []
        self.receivers = []
        self.peers = {}
        self.must_stop = False
        self.injector = EventInjector()
        self.thread = threading.Thread(target=self.main_event_loop,
            daemon=True)

        # Load all specified routes by filename or glob pattern.
        for path in routes:
            path = os.path.abspath(path)
            if path.find('*') == -1:
                self.router.load_config(path)
            if path.find('*') >= 0:
                self.router.glob_config(path)

        # Connect signal handlers. TODO: This should be done conditionally
        # to allow running multiple instances in the same thread.
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGHUP, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Invoked when the program receives an interrupt signal
        from the operating system.
        """
        if signum == signal.SIGHUP:
            pass
        if signum in (signal.SIGINT, signal.SIGTERM):
            self.stop()

    def stop(self):
        """Stops sending messages to the AMQP remote and exit the
        main event loop.
        """
        self.must_stop = True
        self.injector.trigger(ApplicationEvent('teardown'))

    def main_event_loop(self):
        """Ensure that the :class:`MessagePublisher` keeps
        receiving beats.
        """
        while True:
            if self.must_stop:
                break
            self.injector.trigger(ApplicationEvent('beat'))
            time.sleep(1/self.framerate)

    def get_peer_address(self, obj):
        """Return the remote AMQP address and port for the given
        :class:`proton.Link` or :class:`proton.Connection`.
        """
        if isinstance(obj, proton.Link):
            obj = obj.connection
        return self.container.get_connection_address(obj)

    def on_beat(self, event):
        """Periodically invoked to force transmission of routed
        messages to the AMQP upstream peer.
        """
        if not self.sendables:
            return

        # TODO: Distribute the messages more intelligently over
        # all AMQP peers.
        self.flush(random.choice(self.sendables))

    def on_teardown(self, event):
        """Close all links, connections and release all other
        resources.
        """

        # Wait for the beat thread to stop before closing the
        # EventInjector.
        self.thread.join()
        self.injector.close()

        # Ensure that all links are closed so that the remote does
        # not get confused.
        for link in self.senders:
            link.close()

        self.container.stop()

    def get_connection(self, addr):
        """Connect to `addr` if it is not established yet and return the
        connection instance.
        """
        if addr not in self.peers:
            self.peers[addr] = self.container.connect(addr)
        return self.peers[addr]

    def on_start(self, event):
        self.container = event.container

        # Connect to the ingress message channel on all AMQP
        # peers.
        for addr in self.remotes:
            connection = self.get_connection(addr)
            self.logger.debug(f'Establishing receiving AMQP link to {addr}/{self.channel}')
            receiver = event.container.create_receiver(connection,
                source=self.channel, name=self.channel)

        # The EventInjector must be started before the child thread
        # starts beating the handler.
        event.container.selectable(self.injector)
        self.thread.start()

        # Connect to each peer and for each peer create an AMQP
        # link for all possible routes.
        routes = self.router.get_possible_routes()
        for addr in self.remotes:
            connection = self.get_connection(addr)
            for channel in routes:
                self.logger.debug(f'Establishing sending AMQP link to {addr}/{channel}')
                sender =event.container.create_sender(connection,
                    target=channel, name=channel)
                self.senders.append(sender)

    ###################################################################
    ##  MESSAGEROUTER BUSINESS LOGIC
    ###################################################################
    def on_message(self, event):
        try:
            self.route(event)
        except Exception:
            self.logger.exception(
                "Caught fatal exception during message routing")

    def on_link_opened(self, event):
        """Invoked when a link with a client is established."""

        # If it is a receiving link, increase its credit to 1000.
        if event.link.is_receiver:
            event.link.flow(1000)

    def on_link_opening(self, event):
        """Invoked when the remote AMQP peer initiates a link."""
        # We don't send messages to clients, so refuse to create a
        # proton.Sender link if it is not originating from our
        # upstream hosts.
        if event.link.is_sender:
            peer = self.get_peer_address(event.link)

    def route(self, event):
        m = event.message
        d = event.delivery
        l = event.link

        for route in self.router.route(m):
            self.logger.debug("Routing delivery %s to %s (peer: %s)",
                d.tag, route, self.get_peer_address(l))
            m.address = route
            self.ingress[route].append((m, d))

        #l.flow(1)
        #self.settle(d, Disposition.ACCEPTED)

    def flush(self, link, limit=100):
        # Ensure that we do not start sending messages if
        # we must stop.
        if self.must_stop:
            return

        destination = link.target.address
        while link.credit and bool(self.ingress[destination]):
            host = self.get_peer_address(link)
            m, d = self.ingress[destination].pop(0)
            self.logger.debug(f"Routing message {m.id} to {destination}")
            u = link.send(m)
            self.egress[u.tag] = d

    def on_message_persisted(self, message):
        if self.sendables:
            self.flush(random.choice(self.sendables))

    ###################################################################
    ##  MESSAGEPUBLISHER BUSINESS LOGIC
    ###################################################################
    def on_sendable(self, event):
        link = event.link
        peer = self.get_peer_address(link)
        self.logger.debug(
            "AMQP link sendable (target: %s, name: %s, host: %s, credit: %s)",
            link.target.address, link.name, self.get_peer_address(link),
            link.credit)
        self.flush(link=link)

    def on_accepted(self, event):
        self.logger.debug("Delivery %s accepted (host: %s)",
            event.delivery.tag, self.get_peer_address(event.link))
        event.delivery.settle()
        self.accept(self.egress[event.delivery.tag])

    def on_rejected(self, event):
        self.logger.warning("Delivery %s rejected (host: %s)",
            event.delivery.tag, self.get_peer_address(event.link))
        event.delivery.settle()

    def on_released(self, event):
        self.logger.warning("Delivery %s released (host: %s)",
            event.delivery.tag, self.get_peer_address(event.link))
        event.delivery.settle()

    def on_settled(self, event):
        event.delivery.settle()
        self.logger.debug("Delivery %s settled (host: %s)",
            event.delivery.tag, self.get_peer_address(event.link))


def main(argv):
    args = parser.parse_args(argv)
    if os.getenv('AORTA_UPSTREAM'):
        args.peers.insert(0, os.environ['AORTA_UPSTREAM'])
    if os.getenv('AORTA_ROUTES'):
        args.routes.insert(0, os.environ['AORTA_ROUTES'])
    handler = MessageRouter(args.peers,
        routes=args.routes, channel=args.ingress_channel,
        loglevel=args.loglevel)
    Container(handler).run()


if __name__ == '__main__':
    main(sys.argv[1:])
