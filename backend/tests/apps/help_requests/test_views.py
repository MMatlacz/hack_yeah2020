import datetime
import uuid

from http import HTTPStatus

from flask import (
    json,
    url_for,
)

import pytest

from flask_jwt_extended import create_access_token
from freezegun import freeze_time

from apps.help_requests import models
from apps.help_requests.geocoding import GeoCodingResult


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

    def test_post_returns_HTTP201_with_created_help_request_data(
        self,
        mocker,
        client,
        user,
    ):
        help_request_data = {
            'address': 'Koszykowa 75, 00-662 Warszawa',
            'name': 'Anonim z MiNI',
            'products': '2 zeszyty, 1 gługis, 10 batonów Snickers',
            'phone_number': '+48 22 62 1 93 1 2',
            'call_time': '04:09 min, today',
            'pickup_time': (
                'dzisiaj wieczorem po 19:35, ale nie pózniej niz o 21:21'
            ),
            'recording_url': (
                '/2010-04-01/Accounts/AC5c58a7435d00847118556e5d9d23fd68/'
                + 'Calls/CA92a85f4890dd2bafc3ee903eccce3c5c/Recordings/'
                + 'REfb609411c0fd2c78b2af9be40bdfa23d.json'
            ),
        }
        geocoding_result = GeoCodingResult(
            help_request_data['address'],
            52.222706,
            21.007007,
        )
        mocker.patch(
            'apps.help_requests.schemas.geolocation_from',
            return_value=geocoding_result,
        )
        response = client.post(
            url_for(self.view_name, _external=False),
            data={'payload': json.dumps(help_request_data)},
        )
        assert response.status_code == HTTPStatus.CREATED
        assert 'Location' in response.headers
        help_request = models.HelpRequest.query.filter_by(
            id=response.json['data']['id'],
        ).one()
        assert help_request.products == help_request_data['products']
        assert help_request.phone_number == '+48226219312'
        assert help_request.address == geocoding_result.address
        assert help_request.latitude == geocoding_result.latitude
        assert help_request.longitude == geocoding_result.longitude
        assert help_request.recording_url.startswith('https://api.twilio.com/')
        assert help_request.recording_url.endswith('.mp3')


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
        assert (
            response.json['data']['products'] == help_request.products.split()
        )
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

    @pytest.mark.parametrize('help_request__accepted_by', [None])
    def test_patch_returns_HTTP200_and_updates_accepted_at_when_accepted_by_updated(
        self,
        client,
        user,
        help_request,
        help_request__accepted_by,
    ):
        datetime_now = datetime.datetime(
            2020,
            1,
            1,
            12,
            47,
            tzinfo=datetime.timezone.utc,
        )
        with freeze_time(datetime_now):
            access_token = create_access_token(user)
            response = client.patch(
                url_for(
                    self.view_name,
                    help_request_id=str(help_request.id),
                    _external=False,
                ),
                headers={'Authorization': f'Bearer {access_token}'},
                json={'accepted_by': str(user.id)},
            )
        assert response.status_code == HTTPStatus.OK
        assert response.json['data']['id'] == str(help_request.id)
        assert response.json['data']['accepted_by'] == str(user.id)
        assert (
            response.json['data']['accepted_at']
            == datetime_now.isoformat(timespec='seconds').split('+', 1)[0]
        )
