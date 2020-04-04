import datetime
import uuid

from http import HTTPStatus

from flask import url_for

import pytest

from flask_jwt_extended import create_access_token


@pytest.mark.flask_db
class TestHelpRequestListView:
    view_name = 'help_requests.help_requests-list'

    def test_get_returns_HTTP200_with_all_unaccepted_help_requests_by_default(
        self,
        client,
        help_request_factory,
        user,
    ):

        help_request_factory.create_batch(10)
        unaccepted_help_requests = help_request_factory.create_batch(
            10,
            accepted_by=None,
        )
        expected_help_request_ids = sorted(
            str(help_request.id) for help_request in unaccepted_help_requests
        )
        access_token = create_access_token(user)
        response = client.get(
            url_for(self.view_name, _external=False),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert response.status_code == HTTPStatus.OK
        help_request_ids = sorted(
            help_request['id'] for help_request in response.json['data']
        )
        assert help_request_ids == expected_help_request_ids

    def test_get_returns_HTTP200_with_all_help_requests_accepted_by_user_with_id_from_filter(
        self,
        client,
        help_request_factory,
        user_factory,
    ):

        help_request_factory.create_batch(10)
        user = user_factory()
        other_user = user_factory()
        help_requests_accepted_by_user = help_request_factory.create_batch(
            10,
            accepted_by=other_user,
        )
        expected_help_request_ids = sorted(
            str(help_request.id)
            for help_request in help_requests_accepted_by_user
        )
        access_token = create_access_token(user)
        response = client.get(
            url_for(self.view_name, _external=False),
            headers={'Authorization': f'Bearer {access_token}'},
            query_string={'accepted_by': str(other_user.id)},
        )
        assert response.status_code == HTTPStatus.OK
        help_request_ids = sorted(
            help_request['id'] for help_request in response.json['data']
        )
        assert help_request_ids == expected_help_request_ids

    def test_get_returns_HTTP200_with_all_help_requests_accepted_by_user_from_request_when_filter_value_is_self(
        self,
        client,
        help_request_factory,
        user,
    ):
        help_request_factory.create_batch(10)
        help_requests_accepted_by_user = help_request_factory.create_batch(
            10,
            accepted_by=user,
        )
        expected_help_request_ids = sorted(
            str(help_request.id)
            for help_request in help_requests_accepted_by_user
        )
        access_token = create_access_token(user)
        response = client.get(
            url_for(self.view_name, _external=False),
            headers={'Authorization': f'Bearer {access_token}'},
            query_string={'accepted_by': 'self'},
        )
        assert response.status_code == HTTPStatus.OK
        help_request_ids = sorted(
            help_request['id'] for help_request in response.json['data']
        )
        assert help_request_ids == expected_help_request_ids


@pytest.mark.flask_db
class TestHelpRequestRetrieveUpdateView:
    view_name = 'help_requests.help_requests-detail'

    def test_get_returns_HTTP200_with_requested_object_representation(
        self,
        client,
        help_request,
        user,
    ):
        access_token = create_access_token(user)
        response = client.get(
            url_for(
                self.view_name,
                help_request_id=str(help_request.id),
                _external=False,
            ),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json['data']['id'] == str(help_request.id)
        assert response.json['data']['things'] == help_request.things
        assert (
            response.json['data']['accepted_by']
            == str(help_request.accepted_by_id)
        )

    def test_get_returns_HTTP404_when_object_does_not_exist(
        self,
        client,
        user,
    ):
        access_token = create_access_token(user)
        response = client.get(
            url_for(
                self.view_name,
                help_request_id=str(uuid.uuid4()),
                _external=False,
            ),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_patch_returns_HTTP200_with_updated_object_representation(
        self,
        client,
        help_request,
        user,
    ):
        finished_at = datetime.datetime(
            2020,
            1,
            1,
            12,
            47,
            tzinfo=datetime.timezone.utc,
        )
        access_token = create_access_token(user)
        response = client.patch(
            url_for(
                self.view_name,
                help_request_id=str(help_request.id),
                _external=False,
            ),
            headers={'Authorization': f'Bearer {access_token}'},
            json={'finished_at': finished_at.isoformat()},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json['data']['id'] == str(help_request.id)
        assert (
            response.json['data']['finished_at']
            == finished_at.isoformat(timespec='seconds').split('+', 1)[0]
        )
