import phonenumbers

from flask_admin.contrib.sqla import ModelView
from wtforms.fields import StringField
from wtforms.validators import (
    DataRequired,
    ValidationError,
)

from apps.extensions import (
    admin,
    db,
)

from . import models


def is_valid_phone_number(form, field):
    try:
        parsed_phone_number = phonenumbers.parse(field.data)
    except (phonenumbers.phonenumberutil.NumberParseException) as exc:
        raise ValidationError(str(exc))
    else:
        if not phonenumbers.is_valid_number(parsed_phone_number):
            raise ValidationError('Invalid phone number')


class HelpRequestModelView(ModelView):
    form_extra_fields = {
        'phone_number': StringField(
            'Phone Number',
            validators=[DataRequired(), is_valid_phone_number],
        ),
    }


admin.add_view(HelpRequestModelView(models.HelpRequest, db.session))
