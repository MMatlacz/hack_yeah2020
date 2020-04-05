from flask_admin.contrib.sqla import ModelView

from apps.extensions import (
    admin,
    db,
)

from . import models


class HelpRequestModelView(ModelView):
    column_display_pk = True


admin.add_view(HelpRequestModelView(models.HelpRequest, db.session))
