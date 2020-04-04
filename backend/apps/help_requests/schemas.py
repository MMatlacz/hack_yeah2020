from marshmallow import fields

from ..extensions import schemas
from . import models


class HelpRequestSchema(schemas.ModelSchema):
    class Meta:
        model = models.HelpRequest
        fields = (
            'id',
            'full_name',
            'phone_number',
            'address',
            'products',
            'pickup_time',
            'call_time',
            'finished_at',
            'accepted_at',
            'accepted_by',
            'created_at',
            'updated_at',
        )
        dump_only = (
            'id',
            'created_at',
            'updated_at',
        )


class HelpRequestCreateSchema(schemas.Schema):
    address = fields.String(required=True)
    full_name = fields.String(required=True, data_key='name')
    products = fields.String(required=True)
    call_time = fields.String(required=True, default='')
    pickup_time = fields.String(required=True)
    phone_number = fields.String(required=True)


class HelpRequestPartialUpdateSchema(HelpRequestSchema):
    class Meta(HelpRequestSchema.Meta):
        dump_only = (
            'id',
            'full_name',
            'phone_number',
            'address',
            'products',
            'pickup_time',
            'call_time',
            'created_at',
            'updated_at',
        )
