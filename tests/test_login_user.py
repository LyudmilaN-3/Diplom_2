import allure
import pytest

from http import HTTPStatus

from sources import urls
from sources.constants import Constants
from sources.user_support import (
    get_response_post_user as response_user,
    login_exist_user as login
)


class TestLoginUser:

    @allure.title('Проверка возможности логина пользователя')
    @allure.issue(f'{urls.MAIN_URL}{urls.UserAPIRoutes.ENDPOINT_USER_LOGIN}')
    def test_login_user_exist_user_available_success(self, get_exist_user_data, delete_fix):
        current_response = login(get_exist_user_data['payload'])
        decod_resp = response_user(current_response)
        delete_fix.update(decod_resp)
        assert decod_resp['status_code'] == HTTPStatus.OK
        assert decod_resp['message_success'] == Constants.RESPONSE_SUCCESS

    @allure.title('Проверка невозможности логина пользователя с неверным логином или паролем')
    @allure.issue(f'{urls.MAIN_URL}{urls.UserAPIRoutes.ENDPOINT_USER_LOGIN}')
    @pytest.mark.parametrize('wrong_field', ['email', 'password'])
    def test_login_user_exist_user_wrong_field_unavailable_success(self, get_exist_user_data, delete_fix, wrong_field):
        current_response = login(get_exist_user_data['payload'], wrong_field)
        decod_resp = response_user(current_response)
        delete_fix.update(token=get_exist_user_data['response'].json())
        assert decod_resp['status_code'] == HTTPStatus.UNAUTHORIZED
        assert decod_resp['message_success'] == Constants.RESPONSE_FAILURE
        assert decod_resp['message'] == Constants.ERROR_MESSAGE_WRONG_FIELD
