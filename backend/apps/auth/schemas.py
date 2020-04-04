from marshmallow import fields
from marshmallow import validate as validators
from typing_extensions import Final

from ..extensions import schemas

MAX_LENGTH: Final[int] = 255


class AuthLoginSchema(schemas.Schema):
    email = fields.Email(
        required=True,
        validate=[validators.Length(min=3, max=MAX_LENGTH)],
    )
    password = fields.String(
        required=True,
        validate=[validators.Length(min=3, max=MAX_LENGTH)],
    )

    class Meta:
        fields = ('email', 'password')
        load_only = fields
