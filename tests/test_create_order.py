import allure
import requests

from http import HTTPStatus

from sources import urls
from sources.constants import Constants
from sources.order_support import (
    get_data_for_create_order as data_order,
    get_response_post_order as response_order
)


class TestCreateOrder:

    @allure.title('Проверка возможности создания заказа')
    @allure.issue(f'{urls.MAIN_URL}{urls.OrderAPIRoutes.ENDPOINT_ORDER_CREATE_GET}')
    def test_create_order_available_success(self, get_exist_user_data, delete_fix, not_valid=False):
        order_data = data_order(get_exist_user_data, not_valid)
        current_response = requests.post(
            url=order_data['url'],
            data=order_data['data'],
            headers=order_data['headers']
        )
        decod_resp = response_order(current_response)
        delete_fix.update(token=get_exist_user_data['response'].json())
        assert decod_resp['status_code'] == HTTPStatus.OK
        assert decod_resp['message_success'] == Constants.RESPONSE_SUCCESS
        assert 'owner_name' in decod_resp

    @allure.title('Проверка возможности создания заказа неавторизованным пользователем')
    @allure.issue(f'{urls.MAIN_URL}{urls.OrderAPIRoutes.ENDPOINT_ORDER_CREATE_GET}')
    def test_create_order_not_auth_available_success(self, get_exist_user_data, delete_fix, not_valid=False):
        order_data = data_order(get_exist_user_data, not_valid)
        current_response = requests.post(url=order_data['url'], data=order_data['data'])
        decod_resp = response_order(current_response)
        delete_fix.update(token=get_exist_user_data['response'].json())
        assert decod_resp['status_code'] == HTTPStatus.OK
        assert decod_resp['message_success'] == Constants.RESPONSE_SUCCESS
        assert 'owner_name' not in decod_resp

    @allure.title('Проверка невозможности создания заказа без ингредиентов')
    @allure.issue(f'{urls.MAIN_URL}{urls.OrderAPIRoutes.ENDPOINT_ORDER_CREATE_GET}')
    def test_create_order_not_ingredients_unavailable_success(self, get_exist_user_data, delete_fix, not_valid=False):
        order_data = data_order(get_exist_user_data, not_valid)
        current_response = requests.post(url=order_data['url'], headers=order_data['headers'])
        decod_resp = response_order(current_response)
        delete_fix.update(token=get_exist_user_data['response'].json())
        assert decod_resp['status_code'] == HTTPStatus.BAD_REQUEST
        assert decod_resp['message_success'] == Constants.RESPONSE_FAILURE
        assert decod_resp['message'] == Constants.ERROR_MESSAGE_NOT_INGREDIENTS

    @allure.title('Проверка невозможности создания заказа с неверным хешем ингредиента')
    @allure.issue(f'{urls.MAIN_URL}{urls.OrderAPIRoutes.ENDPOINT_ORDER_CREATE_GET}')
    def test_create_order_wrong_hash_ingredient_unavailable_success(
            self, get_exist_user_data, delete_fix, not_valid=True
    ):
        order_data = data_order(get_exist_user_data, not_valid)
        current_response = requests.post(url=order_data['url'], data=order_data['data'], headers=order_data['headers'])
        decod_resp = response_order(current_response)
        delete_fix.update(token=get_exist_user_data['response'].json())
        assert decod_resp['status_code'] == HTTPStatus.INTERNAL_SERVER_ERROR
        assert current_response.ok is False
