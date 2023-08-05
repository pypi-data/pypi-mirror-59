import functools
import logging


class MessageHandlerMeta(type):

    def __new__(cls, name, bases, attrs):
        super_new = super(MessageHandlerMeta, cls).__new__
        if name in ['MessageHandler']:
            return super_new(cls, name, bases, attrs)

        attrs.update({'_handles': set()})
        new_class = super_new(cls, name, bases, attrs)
        return new_class


class MessageHandler(metaclass=MessageHandlerMeta):
    """A base class that abstracts the various handling stages of an
    AMQP message.
    """
    #: Indicates if the message handler is a consumer i.e. the
    #: infrastructure must not propagate the message to other
    #: handlers.
    is_consumer = False

    #: Instructs the handler to treat message validation errors
    #: as errors instead of dropping the message.
    strict = False

    #: The default logger for message handlers
    logger = logging.getLogger('aorta.handlers')

    #: Specifies the default serializer class for incoming
    #: messages.
    serializer_class = None

    #: The default serializer arguments.
    serializer_args = None

    class Rejected(Exception):
        """Raised when the handler wants to reject the message."""
        pass

    @staticmethod
    def register_for(name):
        """Registers the message handler to receive messages that
        have the canonical name `name`.
        """
        def class_decorator(cls):
            cls._handles.add(name)
            return cls
        return class_decorator

    @classmethod
    def add_to_provider(cls, provider):
        """Adds the message handler to a provider implementation."""
        for canonical_name in cls._handles:
            provider.on_canonical(canonical_name, cls)

    @classmethod
    def run(cls, runner, context):
        handler = cls(context)
        try:
            # The body of Aorta-compliant AMQP messages is always
            # a dictionary.
            context.handle(handler.handle,
                serializer=handler.get_serializer())
        except handler.Rejected:
            context.on_rejected(handler)
            runner.reject()
        except Exception as e:
            handler.logger.exception("Caugt fatal %s",
                type(e).__name__)
            handler.set_exception(e)
            handler.on_exception(e)
        finally:
            handler.on_finished()

    def __init__(self, context):
        self.context = context
        self.exception = None

    def set_exception(self, exception):
        """Sets the exception to the handler for post-processing."""
        self.exception = exception

    def get_serializer(self, *args, **kwargs):
        """Return the serializer instance that should be used
        for validating and deserializing input.
        """
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)\
            if serializer_class else None

    def get_serializer_class(self):
        """Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide
        different deserializations depending on the incoming
        message.
        """
        return self.serializer_class

    def handle(self, params):
        """Executes business logic with the message payload as the
        parameters.
        """
        self.logger.warning("Subclasses must implement this method.")

    def on_exception(self, exception):
        """Invoked when an exception is raised during message
        handling.
        """
        pass

    def on_rejected(self, message, dto):
        """Invoked when the handler rejects a message."""
        pass

    def on_finished(self):
        """Invoked when the runner is done handling the message for
        this handler class.
        """
        pass

    def observe(self, *args, **kwargs):
        """Observe an event within the context of the current
        message.
        """
        return self.context.observe(*args, **kwargs)

    def observemany(self, events, *args, **kwargs):
        """Like :meth:`observe()`, but publish all events over a
        single connection. Use for batch operations.
        """
        return self.context.observemany(events, *args, **kwargs)

    def issue(self, *args, **kwargs):
        """Issue a command within the context of the current
        message.
        """
        return self.context.issue(*args, **kwargs)

    def reject(self):
        """Rejects the current message."""
        raise self.Rejected
