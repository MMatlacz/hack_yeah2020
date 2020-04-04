from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .common.extensions.socketio import SocketIO
from .task_app.extensions import Celery

db = SQLAlchemy()
migrate = Migrate(db=db)
schemas = Marshmallow()
celery_extension = Celery()
jwt = JWTManager()
socketio = SocketIO()
