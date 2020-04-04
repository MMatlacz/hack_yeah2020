import typing

import flask

import celery


class AppContextTask(celery.Task):
    """Celery task running within a Flask application context.

    Expects the associated Flask application to be set on the bound
    Celery application.
    """

    abstract: bool = True

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        # If an "app_context" has already been loaded, just pass through
        if flask._app_ctx_stack.top is not None:  # noqa: WPS437
            return super().__call__(*args, **kwargs)
        with self.app.flask_app.app_context():
            return super().__call__(*args, **kwargs)


# TODO: refactor it to be `Celery` instance, so it could be used directly
class Celery:
    def __init__(self, app: typing.Optional[flask.Flask] = None) -> None:
        self.app = app
        self.celery = None
        if app is not None:
            self.init_app(app)

    def init_app(
        self,
        app: flask.Flask,
        celery_app: typing.Optional[celery.Celery] = None,
    ) -> None:
        self.celery = celery_app or celery.current_app
        self.celery.config_from_object(app.config, namespace='CELERY')
        self.celery.Task = AppContextTask
        # set Flask application object on the Celery application.
        self.celery.flask_app = app
        installed_apps = [
            blueprint_path.rsplit(':', 1)[0]
            for blueprint_path in app.config['INSTALLED_BLUEPRINTS']
        ]
        installed_apps.append('apps.task_app')
        self.celery.autodiscover_tasks(installed_apps, force=True)
