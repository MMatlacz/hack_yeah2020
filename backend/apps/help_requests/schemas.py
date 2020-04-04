from ..extensions import schemas
from . import models


class HelpRequestSchema(schemas.ModelSchema):
    class Meta:
        model = models.HelpRequest
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'address',
            'things',
            'finished_at',
            'accepted_at',
            'accepted_by',
            'created_at',
            'updated_at',
        )
        dump_only = (
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'address',
            'things',
            'created_at',
            'updated_at',
        )
