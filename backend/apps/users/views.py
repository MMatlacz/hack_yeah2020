from http import HTTPStatus

from flask import (
    request,
    url_for,
)

from flask_jwt_extended import (
    current_user,
    jwt_required,
)

from apps.common.views import APIView
from apps.common.wrappers.response import JSONResponse

from ..extensions import db
from . import (
    models,
    schemas,
)


class UserCreateView(APIView):
    def post(self) -> JSONResponse:
        user = schemas.UserSchema().load(request.json)
        db.session.add(user)
        db.session.commit()
        return JSONResponse(
            {'data': schemas.UserSchema(exclude=('password',)).dump(user)},
            HTTPStatus.CREATED,
            headers={
                'Location': url_for('.user-detail', user_id=str(user.id)),
            },
        )


class UserRetrieveView(APIView):
    method_decorators = [jwt_required]

    def get(self, user_id: str) -> JSONResponse:
        if user_id == 'self':
            user = current_user
        else:
            # TODO: add exception handler that handle sqlachemy exceptions
            # like `NoResultFound` and return `HTTP_404` response with proper
            # message
            user = models.User.query.get(user_id)
        return JSONResponse(
            {'data': schemas.UserSchema().dump(user)},
            HTTPStatus.OK,
        )
