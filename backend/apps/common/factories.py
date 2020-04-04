import importlib

import factory

from flask_sqlalchemy.model import Model

from apps.extensions import db


class SQLAlchemyOptions(factory.alchemy.SQLAlchemyOptions):
    def get_model_class(self) -> Model:
        if isinstance(self.model, str):
            module_path, factory_class_name = self.model.rsplit('.', 1)
            factories_module = importlib.import_module(module_path)
            return getattr(factories_module, factory_class_name)
        return super().get_model_class()

    @property
    def sqlalchemy_session(self):
        """``Flask-SQLAlchemy`` scoped session.

        This is necessary to properly mock session in tests.
        """
        return db.session

    def _build_default_options(self):
        return [
            option
            for option in super()._build_default_options()
            if option.name != 'sqlalchemy_session'
        ]


class SQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    _options_class = SQLAlchemyOptions

    class Meta:
        abstract = True
        sqlalchemy_session_persistence = 'commit'
