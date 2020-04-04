import uuid

from http import HTTPStatus

from flask import url_for

import pytest

from flask_jwt_extended import create_access_token


@pytest.mark.flask_db(transaction=True)
class TestAuthJWTTokenCreateView:
    view_name = 'auth.jwt_token-list'

    @pytest.mark.parametrize('user__password', ['testingpass123'])
    def test_post_returns_access_token_when_user_credentials_valid(
        self,
        client,
        flask_app,
        user,
        user__password,
    ):
        data = {'email': user.email, 'password': user__password}
        response = client.post(url_for(self.view_name), json=data)
        assert response.status_code == HTTPStatus.OK
        assert response.json[flask_app.config['JWT_JSON_KEY']]

    @pytest.mark.parametrize('user__password', ['testingpass123'])
    def test_post_returns_HTTP401_with_error_message_when_password_invalid(
        self,
        client,
        user,
        user__password,
    ):
        data = {'email': user.email, 'password': 'definitely not a valid pass'}
        response = client.post(url_for(self.view_name), json=data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json['message'].lower() == 'invalid credentials'

    @pytest.mark.parametrize('user__password', ['testingpass123'])
    @pytest.mark.parametrize('user__email', ['test-me@likeyou.do'])
    def test_post_returns_HTTP401_with_error_message_when_email_invalid(
        self,
        client,
        user,
        user__password,
    ):
        data = {'email': 'john.cleese@ni.ni', 'password': user__password}
        response = client.post(url_for(self.view_name), json=data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json['message'].lower() == 'invalid credentials'

    def test_delete_returns_HTTP200_when_valid_token_provided(
        self,
        client,
        user,
    ):
        access_token = create_access_token(user)
        response = client.delete(
            url_for(self.view_name),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert response.status_code == HTTPStatus.OK

    def test_delete_returns_HTTP401_when_access_token_not_provided(
        self,
        client,
    ):
        response = client.delete(url_for(self.view_name))
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_delete_returns_HTTP404_when_access_token_owner_does_not_exist(
        self,
        client,
        user_factory,
    ):
        access_token = create_access_token(
            user_factory.build(id=uuid.uuid4().hex),
        )
        response = client.delete(
            url_for(self.view_name),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
