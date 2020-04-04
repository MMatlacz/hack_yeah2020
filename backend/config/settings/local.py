import os

from .base import *

# FLASK
DEBUG = True
ENV = env('FLASK_ENV', default='development')
SECRET_KEY_LENGTH = 16
SECRET_KEY = env('FLASK_SECRET_KEY', default=str(os.urandom(SECRET_KEY_LENGTH)))

# DATABASES
SQLALCHEMY_ECHO = DEBUG

# AUTHENTICATION
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(
    seconds=env.int(
        'JWT_ACCESS_TOKEN_EXPIRES',
        default=datetime.timedelta(days=3).total_seconds(),
    ),
)
JWT_SECRET_KEY = env('JWT_SECRET_KEY', default=SECRET_KEY)


# SOCKET.IO
SOCKETIO_LOGGER = True
SOCKETIO_ENGINEIO_LOGGER = True
