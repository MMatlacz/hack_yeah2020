from http import HTTPStatus

from flask import current_app

from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from .wrappers.response import JSONResponse


@current_app.errorhandler(ValidationError)
def handle_marshmallow_ValidationError(
    exception: ValidationError,
) -> JSONResponse:
    return JSONResponse(
        exception.normalized_messages(),
        HTTPStatus.BAD_REQUEST,
    )


@current_app.errorhandler(NoResultFound)
def handle_sqlalchemy_orm_NoResultFound(
    exception: NoResultFound,
) -> JSONResponse:
    return JSONResponse({'message': 'Not found'}, HTTPStatus.NOT_FOUND)
