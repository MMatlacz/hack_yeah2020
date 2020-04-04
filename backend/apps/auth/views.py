from http import HTTPStatus

from flask import (
    current_app,
    request,
)

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
)
from sqlalchemy.orm.exc import (
    MultipleResultsFound,
    NoResultFound,
)

from apps.common.views import APIView
from apps.common.wrappers.response import JSONResponse
from apps.users.models import User

from . import schemas


class AuthJWTTokenCreateView(APIView):
    method_decorators = {'delete': [jwt_required]}

    def post(self) -> JSONResponse:
        data = schemas.AuthLoginSchema().load(request.json)
        invalid_credentials_response = JSONResponse(
            {'message': 'Invalid credentials'},
            HTTPStatus.UNAUTHORIZED,
        )
        try:
            user = User.query.filter_by(email=data['email']).one()
        except (NoResultFound, MultipleResultsFound):
            return invalid_credentials_response
        if user.password != data['password']:
            return invalid_credentials_response
        access_token = create_access_token(identity=user)
        return JSONResponse(
            {current_app.config['JWT_JSON_KEY']: access_token},
            HTTPStatus.OK,
        )

    def delete(self) -> JSONResponse:
        # TODO: blacklist token
        return JSONResponse(None, HTTPStatus.OK)
