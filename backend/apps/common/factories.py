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


class SQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    _options_class = SQLAlchemyOptions

    class Meta:
        abstract = True
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
