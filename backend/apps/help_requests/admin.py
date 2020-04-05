from flask import flash

from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView

from apps.extensions import (
    admin,
    db,
)

from . import models


class HelpRequestModelView(ModelView):
    column_display_pk = True

    @action(
        'clear_accepted_by',
        'Clear accepted_by',
        (
            'Are you sure you want to clear `accepted_by` field for '
            + 'selected help requests?'
        ),
    )
    def clear_accepted_by(self, ids):
        try:
            self.session.bulk_update_mappings(
                self.model,
                [
                    {'id': user_id, 'accepted_by_id': None, 'accepted_at': None}
                    for user_id in ids
                ],
            )
            self.session.flush()
            self.session.commit()
            flash(
                f'Successfully cleared accepted_by of {len(ids)} help requests',
                'success',
            )
        except Exception as exc:
            if not self.handle_view_exception(exc):
                raise

            flash(f'Failed to clear approved_by. {exc}', 'error')


admin.add_view(HelpRequestModelView(models.HelpRequest, db.session))
