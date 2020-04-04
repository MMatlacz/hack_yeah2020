import typing
import uuid

from http import HTTPStatus

from flask import (
    Response,
    jsonify,
)

from apps.users.models import User

from ..extensions import jwt

IdentityType = typing.Union[str, uuid.UUID]


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> uuid.UUID:
    return user.id


@jwt.user_loader_callback_loader
def user_loader_callback(identity: IdentityType) -> typing.Optional[User]:
    user = User.query.get(identity)
    if not getattr(user, 'is_active', False):
        return None
    return user


@jwt.user_loader_error_loader
def user_does_not_exists_handler(identity: IdentityType) -> Response:
    return (
        jsonify({'message': 'Given token owner does not exist.'}),
        HTTPStatus.NOT_FOUND,
    )
