from http import HTTPStatus

from flask import (
    Response,
    current_app,
    json,
)

from marshmallow import ValidationError


@current_app.errorhandler(ValidationError)
def handle_marshmallow_ValidationError(exception: ValidationError) -> Response:
    return Response(
        json.dumps(exception.normalized_messages()),
        HTTPStatus.BAD_REQUEST,
        headers={'Content-Type': 'application/json'},
    )
