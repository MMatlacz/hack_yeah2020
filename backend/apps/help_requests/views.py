from http import HTTPStatus

from flask import request

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


class HelpRequestListView(APIView):
    method_decorators = [jwt_required]

    def get(self) -> JSONResponse:
        accepted_by = request.args.get('accepted_by', None)
        if accepted_by == 'self':
            accepted_by = current_user.id
        help_requests = models.HelpRequest.query.filter_by(
            accepted_by_id=accepted_by,
        )
        return JSONResponse(
            {'data': schemas.HelpRequestSchema(many=True).dump(help_requests)},
            HTTPStatus.OK,
        )


class HelpRequestRetrieveUpdateView(APIView):
    method_decorators = [jwt_required]

    def get(self, help_request_id: str) -> JSONResponse:
        help_request = models.HelpRequest.query.filter_by(
            id=help_request_id,
        ).one()
        return JSONResponse(
            {'data': schemas.HelpRequestSchema().dump(help_request)},
            HTTPStatus.OK,
        )

    def patch(self, help_request_id: str) -> JSONResponse:
        help_request = models.HelpRequest.query.filter_by(
            id=help_request_id,
        ).one()
        help_request_data = request.json
        help_request = schemas.HelpRequestSchema().load(
            help_request_data,
            instance=help_request,
        )
        db.session.add(help_request)
        db.session.commit()
        return JSONResponse(
            {'data': schemas.HelpRequestSchema().dump(help_request)},
            HTTPStatus.OK,
        )
