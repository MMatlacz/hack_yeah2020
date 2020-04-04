import importlib
import inspect

import inflection
import pytest

from factory import Factory
from pytest_factoryboy import register
from sqlalchemy_utils import functions

from apps.application import create_app
from apps.extensions import db as database

FACTORIES_MODULE_PATHS = (
    'apps.users.factories',
)


def _get_model_name(factory_class):
    model_class = factory_class._meta.model
    if isinstance(model_class, str):
        model_name = model_class.rsplit('.', 1)[-1]
    else:
        model_name = model_class.__name__
    return inflection.underscore(model_name)


def register_factories(factories_module_paths):
    for factories_module_path in factories_module_paths:
        factories_module = importlib.import_module(factories_module_path)
        for name, factory_wannabe in factories_module.__dict__.items():
            if name.startswith('_'):
                continue
            if (
                    inspect.isclass(factory_wannabe)
                    and issubclass(factory_wannabe, Factory)
                    and not factory_wannabe._meta.abstract
            ):
                register(
                    factory_wannabe,
                    _name=_get_model_name(factory_wannabe),
                )


def pytest_sessionstart():
    register_factories(FACTORIES_MODULE_PATHS)


@pytest.fixture(autouse=True)
def _flask_db_marker(request):
    marker = request.node.get_closest_marker('flask_db')
    if marker:
        transaction = validate_flask_db(marker)
        if transaction:
            request.getfixturevalue('transaction_free_session')
        else:
            request.getfixturevalue('session')


def validate_flask_db(marker):
    def attach_attributes(transaction=False):
        return transaction

    return attach_attributes(*marker.args, **marker.kwargs)


@pytest.fixture(scope='session')
def flask_app(request):
    app = create_app('config.settings.test')
    app_context = app.app_context()
    app_context.push()
    yield app
    app_context.pop()


@pytest.fixture(scope='session')
def client(flask_app):
    return flask_app.test_client()


@pytest.fixture(scope='session')
def db(flask_app):
    database.app = flask_app
    if functions.database_exists(database.engine.url):
        functions.drop_database(database.engine.url)
    functions.create_database(database.engine.url)
    database.create_all()
    yield database
    database.session.remove()
    database.drop_all()


@pytest.fixture(scope='function')
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()
    session = db.create_scoped_session(
        options={'bind': connection, 'binds': {}},
    )
    initial_session = db.session
    db.session = session
    yield session
    transaction.rollback()
    connection.close()
    session.remove()
    db.session = initial_session


@pytest.fixture(scope='function')
def transaction_free_session(db, request):
    yield db.session
    db.session.remove()
    db.drop_all()
    db.create_all()
