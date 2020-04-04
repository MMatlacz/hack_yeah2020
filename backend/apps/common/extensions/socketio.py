from flask import Flask

from flask_socketio import SocketIO as BaseSocketIO
from typing_extensions import Final

DEFAULT_SOCKETIO_SETTINGS_NAMESPACE: Final = 'SOCKETIO_'


class SocketIO(BaseSocketIO):
    def init_app(self, app: Flask, **kwargs) -> None:
        namespace = app.config.get(
            'SOCKETIO_SETTINGS_NAMESPACE',
            DEFAULT_SOCKETIO_SETTINGS_NAMESPACE,
        )
        kwargs.update(app.config.get_namespace(namespace, lowercase=True))
        return super().init_app(app, **kwargs)
