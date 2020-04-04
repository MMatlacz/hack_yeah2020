from .base import *

# FLASK
DEBUG = False
ENV = 'test'
TESTING = True
SECRET_KEY = 'testing_super_secret_key'
SERVER_NAME = 'testing.server'


# DATABASES
SQLALCHEMY_ECHO = DEBUG
# use separate DB in tests
DB_NAME = f'test__{DB_NAME}'
SQLALCHEMY_DATABASE_URI = 'postgres://{0}:{1}@{2}:{3}/{4}'.format(
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
)


# SECURITY
PASSWORD_SCHEMES = ('md5_crypt',)


# AUTHENTICATION
JWT_SECRET_KEY = 'testing_super_secret_JWT_key'


# CELERY
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
