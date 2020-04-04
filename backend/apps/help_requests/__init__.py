from apps.common.blueprints import Blueprint

help_requests_app = Blueprint(
    'help_requests',
    __name__,
    url_prefix='/help-requests',
)
