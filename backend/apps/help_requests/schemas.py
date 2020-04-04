from marshmallow import fields

from ..extensions import schemas
from . import models


class HelpRequestSchema(schemas.ModelSchema):
    products = fields.Method(
        serialize='get_products',
        deserialize='load_products',
    )

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

    def get_products(self, obj):  # noqa: WPS110
        products = obj.products or ''
        return products.split()

    def load_products(self, value):  # noqa: WPS110
        return str(value)


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
