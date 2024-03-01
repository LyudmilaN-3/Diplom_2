import allure
import requests

from http import HTTPStatus

from sources import urls
from sources.constants import Constants
from sources.order_support import (
    get_data_for_create_order as data_order,
    get_response_post_order as response_order
)


class TestGetOrdersUser:

    @allure.title('Проверка возможности получения заказов пользователя')
    @allure.issue(urls.POST_GET_ORDER_ROUTE)
    def test_get_orders_user_available_success(self, get_exist_user_data, delete_fix, not_valid=False):
        order_data = data_order(get_exist_user_data, not_valid)
        current_response = requests.get(url=order_data['url'], headers=order_data['headers'])
        decod_resp = response_order(current_response)
        delete_fix.update(token=get_exist_user_data['response'].json())
        assert decod_resp['status_code'] == HTTPStatus.OK
        assert decod_resp['message_success'] == Constants.RESPONSE_SUCCESS
        assert 'total' in decod_resp

    @allure.title('Проверка невозможности получения заказов неавторизованного пользователя')
    @allure.issue(urls.POST_GET_ORDER_ROUTE)
    def test_get_orders_not_auth_user_unavailable_success(self, get_exist_user_data, delete_fix, not_valid=False):
        order_data = data_order(get_exist_user_data, not_valid)
        current_response = requests.get(url=order_data['url'])
        decod_resp = response_order(current_response)
        delete_fix.update(token=get_exist_user_data['response'].json())
        assert decod_resp['status_code'] == HTTPStatus.UNAUTHORIZED
        assert decod_resp['message'] == Constants.ERROR_MESSAGE_NOT_AUTH
        assert 'total' not in decod_resp
