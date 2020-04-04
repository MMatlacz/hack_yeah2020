from . import (
    help_requests_app,
    views,
)

help_requests_app.add_url_rule(
    '/<help_request_id>',
    'help_requests-detail',
    views.HelpRequestRetrieveUpdateView.as_view('help_requests-detail'),
)
help_requests_app.add_url_rule(
    '/',
    'help_requests-list',
    views.HelpRequestListView.as_view('help_requests-list'),
)
