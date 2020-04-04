from http import HTTPStatus

from flask import url_for

import pytest

from flask_jwt_extended import create_access_token

from apps.users import models


@pytest.mark.flask_db
class TestUserCreateView:
    view_name = 'users.user-list'

    @pytest.fixture
    def user_schema_load_data(self):
        return {
            'first_name': 'John',
            'last_name': 'Cleese',
            'username': 'johnnie',
            'email': 'john.cleese@monty.python',
            'password': 'super_secret123',
        }

    def test_post_creates_new_user_with_given_data_when_user_with_following_email_does_not_exist(
        self,
        client,
        user_schema_load_data,
    ):
        response = client.post(
            url_for(self.view_name, _external=False),
            json=user_schema_load_data,
        )
        assert response.status_code == HTTPStatus.CREATED
        user_id = response.json['data']['id']
        user = models.User.query.get(user_id)
        for field_name, field_value in user_schema_load_data.items():
            assert getattr(user, field_name) == field_value

    def test_post_creates_set_Location_header_to_URL_pointing_to_user_details(
        self,
        client,
        user_schema_load_data,
    ):
        response = client.post(
            url_for(self.view_name, _external=False),
            json=user_schema_load_data,
        )
        assert response.status_code == HTTPStatus.CREATED
        assert (
            response.headers['Location'].endswith(
                f'users/{response.json["data"]["id"]}',
            )
        )

    def test_post_returns_HTTP400_with_error_message_when_use_with_given_email_already_exists(
        self,
        client,
        user,
        user_schema_load_data,
    ):
        user_schema_load_data['email'] = user.email
        response = client.post(
            url_for(self.view_name, _external=False),
            json=user_schema_load_data,
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert 'email' in response.json


@pytest.mark.flask_db
class TestUserRetrieveView:
    view_name = 'users.user-detail'

    def test_get_returns_authenticated_user_when_user_id_equals_to_self(
        self,
        client,
        user_factory,
    ):
        users = user_factory.create_batch(10)
        user = users[4]
        access_token = create_access_token(user)
        response = client.get(
            url_for(self.view_name, user_id='self', _external=False),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json['data']['id'] == str(user.id)

    def test_get_returns_concrete_user_when_user_id_equal_to_uuid(
        self,
        client,
        user_factory,
    ):
        users = user_factory.create_batch(10)
        user = users[4]
        access_token = create_access_token(users[0])
        response = client.get(
            url_for(self.view_name, user_id=user.id, _external=False),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json['data']['id'] == str(user.id)
