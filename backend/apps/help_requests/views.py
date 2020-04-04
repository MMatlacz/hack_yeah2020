import datetime

from http import HTTPStatus

from flask import (
    request,
    url_for,
)

from flask_jwt_extended import (
    current_user,
    jwt_required,
)
from typing_extensions import Final

from apps.common.views import APIView
from apps.common.wrappers.response import JSONResponse
from apps.users.models import User

from ..extensions import db
from . import (
    models,
    schemas,
)

RESPONSE_DATA_KEY: Final[str] = 'data'


class HelpRequestCreateListView(APIView):
    method_decorators = {'get': [jwt_required]}

    def get(self) -> JSONResponse:
        accepted_by = request.args.get('accepted_by', None)
        if accepted_by == 'self':
            accepted_by = current_user.id
        help_requests = models.HelpRequest.query.filter_by(
            accepted_by_id=accepted_by,
        )
        return JSONResponse(
            {
                RESPONSE_DATA_KEY: schemas.HelpRequestSchema(many=True).dump(
                    help_requests,
                ),
            },
            HTTPStatus.OK,
        )

    def post(self) -> JSONResponse:
        help_request_data = schemas.HelpRequestCreateSchema().load(request.json)
        help_request = schemas.HelpRequestSchema().load(help_request_data)
        db.session.add(help_request)
        db.session.commit()
        return JSONResponse(
            {RESPONSE_DATA_KEY: schemas.HelpRequestSchema().dump(help_request)},
            HTTPStatus.CREATED,
            headers={
                'Location': url_for(
                    '.help_requests-detail',
                    help_request_id=str(help_request.id),
                ),
            },
        )


class HelpRequestRetrieveUpdateView(APIView):
    method_decorators = [jwt_required]

    def get(self, help_request_id: str) -> JSONResponse:
        help_request = models.HelpRequest.query.filter_by(
            id=help_request_id,
        ).one()
        return JSONResponse(
            {RESPONSE_DATA_KEY: schemas.HelpRequestSchema().dump(help_request)},
            HTTPStatus.OK,
        )

    def patch(self, help_request_id: str) -> JSONResponse:
        help_request = models.HelpRequest.query.filter_by(
            id=help_request_id,
        ).one()
        help_request_data = request.json
        accepted_by = help_request_data.pop('accepted_by', '')
        if accepted_by:
            if accepted_by == 'self':
                user = current_user
            else:
                user = User.query.filter_by(id=accepted_by).one()
            help_request.accepted_by = user
            help_request.accepted_at = datetime.datetime.now(
                tz=datetime.timezone.utc,
            )
        help_request = schemas.HelpRequestPartialUpdateSchema().load(
            help_request_data,
            instance=help_request,
        )
        db.session.add(help_request)
        db.session.commit()
        return JSONResponse(
            {RESPONSE_DATA_KEY: schemas.HelpRequestSchema().dump(help_request)},
            HTTPStatus.OK,
        )
