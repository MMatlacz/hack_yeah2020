import logging

from typing import (
    Any,
    Callable,
    ClassVar,
    Iterable,
    Mapping,
    Optional,
    Union,
)

from flask_socketio import (
    Namespace,
    SocketIO,
    join_room,
    leave_room,
    rooms,
)

IterableOfDecorators = Iterable[Callable]
EventDecorators = Union[
    Mapping[str, IterableOfDecorators],
    IterableOfDecorators,
]
logger = logging.getLogger(__name__)


class SocketIOConsumer(Namespace):
    """Custom ``flask_socketio.Namespace`` subclass.

    Following class makes working with `flask_socketio` simpler
    and more like working with `django_channels` consumers.

    Attributes
    ----------
    event_decorators
        decorators that will be applied on event handlers.
        When set to mapping, keys are events' names and values are
        iterables of decorators that will be applied to event handler.
        If ``event_decorators`` are set to list then decorators
        will be applied to *every* event.

    """

    event_decorators: ClassVar[Optional[EventDecorators]] = None

    def trigger_event(self, event: str, *args) -> Any:
        event_handler = getattr(self, f'on_{event}', None)
        if not event_handler:
            # there is no handler for this event, so we ignore it
            logger.warning(
                f'Missing "{event}" handler for namespace: "{self.namespace}"',
            )
            return None

        # apply decorators
        event_decorators = self.event_decorators or []
        if isinstance(event_decorators, Mapping):
            event_decorators = event_decorators.get(event.lower(), [])
        for decorator in event_decorators:
            event_handler = decorator(event_handler)
        return self.socketio._handle_event(  # noqa: WPS437
            event_handler,
            event,
            self.namespace,
            *args,
        )

    def join_room(
        self,
        room: str,
        sid: Optional[str] = None,
        namespace: Optional[str] = None,
    ) -> None:
        join_room(room, sid, namespace or self.namespace)

    def leave_room(
        self,
        room: str,
        sid: Optional[str] = None,
        namespace: Optional[str] = None,
    ) -> None:
        leave_room(room, sid, namespace or self.namespace)

    @property
    def rooms(self) -> Iterable[str]:
        return rooms(namespace=self.namespace)

    def _set_socketio(self, socketio: SocketIO) -> None:
        super()._set_socketio(socketio)
        exception_handler = getattr(self, 'exception_handler', None)
        if exception_handler:
            self.socketio.on_error(self.namespace)(exception_handler)
