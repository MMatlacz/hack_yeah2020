import importlib
import logging
import typing

import flask

from flask_socketio import (
    Namespace,
    SocketIO,
)
from typing_extensions import Final

BLUEPRINT_RELATIVE_IMPORTS: Final = (
    ('.models',),
    ('.urls', '.views'),
    ('.routing', '.consumers'),
    ('.hooks',),
    ('.exceptions',),
    ('.admin', '.admins'),
)
SocketIOExceptionHandlerType = typing.Callable[[Exception], typing.Any]
logger: logging.Logger = logging.getLogger(__name__)


def import_blueprint(blueprint_path: str) -> flask.Blueprint:
    """Import first `Blueprint` from `blueprint_path`.

    Parameters
    ----------
    blueprint_path
        path to module contaoing ``Blueprint`` instance
        or to concrete ``Blueprint`` instance. Example values:

        + 'apps.users` - then all `Blueprint` instances will
           be searched in module globals
        + 'apps.users:users_app' - will directly import ``users_app``
           from `app.users` module

    """
    blueprint_module_path, *blueprint_name = blueprint_path.rsplit(':', 1)
    blueprint_module = importlib.import_module(blueprint_module_path)
    if blueprint_name:
        return getattr(blueprint_module, blueprint_name[0])
    for _, module_member in blueprint_module.__dict__.items():  # noqa: WPS609
        if isinstance(module_member, flask.Blueprint):
            return module_member


def register_blueprint(flask_app: flask.Flask, blueprint_path: str) -> None:
    """Register ``Blueprint`` instance in ``flask_app`` registry.

    Registration process is quite more complicated than simple:
    ``flask_app.register_blueprint(blueprint)``, because there is need to
    import few other things:

    + HTTP routes (`urls.py` or `views.py`) declarations
    + models (`models.py`) declarations
    + hooks (`hooks.py`) definitions
    + exception handlers (`exceptions.py`) definitions
    + `flask_socketio` routes (`routes.py` or `consumers.py`) declarations

    """
    blueprint = import_blueprint(blueprint_path)
    with flask_app.app_context():
        for relative_modules in BLUEPRINT_RELATIVE_IMPORTS:
            for relative_module in relative_modules:
                try:
                    importlib.import_module(
                        relative_module,
                        blueprint.import_name,
                    )
                except ModuleNotFoundError:
                    logger.info(
                        (
                            f'Cannot find `{blueprint.import_name}'
                            + f'.{relative_module}` module. Skipping..'
                        ),
                    )
                else:
                    break
    flask_app.register_blueprint(blueprint)


class BlueprintSetupState(flask.blueprints.BlueprintSetupState):
    @property
    def socketio_extension(self) -> SocketIO:
        return self.app.extensions['socketio']

    def on_socketio_namespace(self, namespace_handler: Namespace) -> None:
        self.socketio_extension.on_namespace(namespace_handler)

    def on_socketio_error(
        self,
        namespace: str,
        handler: SocketIOExceptionHandlerType,
    ) -> SocketIOExceptionHandlerType:
        return self.socketio_extension.on_error(namespace)(handler)


class Blueprint(flask.Blueprint):
    """Custom ``Blueprint`` declaration.

    The main reason behind using this class is to add possibility
    to register `flask_socketio` routes using ``Blueprint`` instances.

    """

    def make_setup_state(
        self,
        app: flask.Flask,
        options: typing.Dict,
        first_registration: bool = False,
    ) -> flask.blueprints.BlueprintSetupState:
        return BlueprintSetupState(self, app, options, first_registration)

    def add_socketio_route(self, namespace_handler: Namespace) -> None:
        self.record(
            (lambda state: state.on_socketio_namespace(namespace_handler)),
        )

    def add_socketio_route_error_handler(
        self,
        namespace: str,
        handler: SocketIOExceptionHandlerType,
    ) -> SocketIOExceptionHandlerType:
        self.record(lambda state: state.on_socketio_error(namespace, handler))
