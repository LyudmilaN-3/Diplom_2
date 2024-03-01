import allure
import pytest

from http import HTTPStatus

from sources import urls
from sources.constants import Constants
from sources.user_support import (
    get_response_post_user as response_user,
    update_exist_user as update_user
)


class TestUpdateUser:

    @allure.title('Проверка возможности изменения данных пользователя')
    @allure.issue(urls.UPDATE_DELETE_USER_ROUTE)
    @pytest.mark.parametrize('update_field', ['email', 'name'])
    def test_update_user_available_success(self, get_exist_user_data, update_field, delete_fix, not_auth=False):
        update_field_value = get_exist_user_data['payload'][update_field]
        current_response = update_user(get_exist_user_data, not_auth, update_field)
        decod_resp = response_user(current_response)
        update_field_new_value = decod_resp[update_field]
        delete_fix.update(token=get_exist_user_data['response'].json())
        assert decod_resp['status_code'] == HTTPStatus.OK
        assert decod_resp['message_success'] == Constants.RESPONSE_SUCCESS
        assert update_field_new_value != update_field_value

    @allure.title('Проверка невозможности изменения данных пользователя без авторизации')
    @allure.issue(urls.UPDATE_DELETE_USER_ROUTE)
    @pytest.mark.parametrize('update_field', ['email', 'name'])
    def test_update_user_not_auth_unavailable_success(
            self, get_exist_user_data, update_field, delete_fix, not_auth=True
    ):
        current_response = update_user(get_exist_user_data, not_auth, update_field)
        decod_resp = response_user(current_response)
        delete_fix.update(token=get_exist_user_data['response'].json())
        assert decod_resp['status_code'] == HTTPStatus.UNAUTHORIZED
        assert decod_resp['message_success'] == Constants.RESPONSE_FAILURE
        assert decod_resp['message'] == Constants.ERROR_MESSAGE_NOT_AUTH
