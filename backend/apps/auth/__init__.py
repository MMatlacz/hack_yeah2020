from flask import Blueprint

auth_app = Blueprint('auth', __name__, url_prefix='/users/auth')
