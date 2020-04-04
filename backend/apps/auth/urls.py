from . import (
    auth_app,
    views,
)

auth_app.add_url_rule(
    '/tokens',
    'jwt_token-list',
    views.AuthJWTTokenCreateView.as_view('jwt_token-list'),
)
