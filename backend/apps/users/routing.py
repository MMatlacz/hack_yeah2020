from ..extensions import socketio
from . import (
    consumers,
    users_app,
)

# TODO: get prefix from blueprint
users_app.add_socketio_route(consumers.UserSelfConsumer('/users'))
socketio.on_error_default(consumers.exception_handler)
