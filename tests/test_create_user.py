import allure
import pytest

from http import HTTPStatus

from sources import urls
from sources.constants import Constants
from sources.user_support import (
    register_new_user as register,
    get_response_post_user as response_user
)


class TestCreateUser:

    @allure.title('Проверка возможности создания пользователя')
    @allure.issue(f'{urls.MAIN_URL}{urls.UserAPIRoutes.ENDPOINT_USER_CREATE}')
    def test_create_user_available_success(self, get_new_user_data, delete_fix):
        current_response = register(get_new_user_data)
        decod_resp = response_user(current_response)
        delete_fix.update(decod_resp)
        assert decod_resp['status_code'] == HTTPStatus.OK
        assert decod_resp['message_success'] == Constants.RESPONSE_SUCCESS

    @allure.title('Проверка невозможности создания уже зарегистрированного пользователя')
    @allure.issue(f'{urls.MAIN_URL}{urls.UserAPIRoutes.ENDPOINT_USER_CREATE}')
    def test_create_user_as_prev_user_unavailable_success(self, get_new_user_data, delete_fix):
        reg_data = register(get_new_user_data)
        current_response = register(get_new_user_data)
        decod_resp = response_user(current_response)
        delete_fix.update(token=reg_data.json())
        assert decod_resp['status_code'] == HTTPStatus.FORBIDDEN
        assert decod_resp['message_success'] == Constants.RESPONSE_FAILURE
        assert decod_resp['message'] == Constants.ERROR_MESSAGE_FOR_EXIST_USER

    @allure.title('Проверка невозможности создания пользователя при не заполненном обязательном поле')
    @allure.issue(f'{urls.MAIN_URL}{urls.UserAPIRoutes.ENDPOINT_USER_CREATE}')
    @pytest.mark.parametrize('miss_field', ['email', 'password', 'name'])
    def test_create_user_empty_required_field_unavailable_success(self, get_new_user_data, miss_field, delete_fix):
        current_response = register(get_new_user_data, miss_field)
        decod_resp = response_user(current_response)
        delete_fix.update(decod_resp)
        assert decod_resp['status_code'] == HTTPStatus.FORBIDDEN
        assert decod_resp['message_success'] == Constants.RESPONSE_FAILURE
        assert decod_resp['message'] == Constants.ERROR_MESSAGE_EMPTY_REQUIRED_FIELD
