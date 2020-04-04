from marshmallow import (
    ValidationError,
    fields,
)
from marshmallow import validate as validators
from marshmallow import validates
from marshmallow_sqlalchemy import field_for

from ..extensions import schemas
from . import models


class UserSchema(schemas.ModelSchema):
    email = fields.Email(
        required=True,
        validate=[validators.Length(min=3, max=255)],  # noqa: WPS432
    )
    password = field_for(
        models.User,
        'password',
        required=True,
        load_only=True,
    )
    created_at = field_for(models.User, 'created_at', dump_only=True)

    class Meta:
        model = models.User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'username',
            'password',
            'created_at',
        )

    @validates('email')
    def validate_email(self, email: str, **kwargs) -> None:
        if models.User.query.filter_by(email=email).scalar():
            raise ValidationError('User with given email already exists')
