from marshmallow import (
    fields,
    post_load,
)

from ..extensions import schemas
from . import models
from .geocoding import geolocation_from


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
            'latitude',
            'longitude',
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
    address = fields.String(required=True, load_only=True)
    full_name = fields.String(required=True, load_only=True, data_key='name')
    products = fields.String(required=True, load_only=True)
    call_time = fields.String(required=True, load_only=True, default='')
    pickup_time = fields.String(required=True, load_only=True)
    phone_number = fields.String(required=True, load_only=True)

    @post_load
    def make_object(self, data, **kwargs):
        data.update(
            geolocation_from(data['address'])._asdict(),  # noqa: WPS437
        )
        data['phone_number'] = ''.join(
            char for char in data['phone_number']
            if char.isdigit() or char == '+'
        )
        return data


class HelpRequestPartialUpdateSchema(HelpRequestSchema):
    class Meta(HelpRequestSchema.Meta):
        dump_only = (
            'id',
            'full_name',
            'phone_number',
            'address',
            'latitude',
            'longitude',
            'products',
            'pickup_time',
            'call_time',
            'created_at',
            'updated_at',
        )
