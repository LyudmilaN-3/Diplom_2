import allure

from sources.constants import Constants
from sources import data, urls


@allure.step('Формирование тела запроса')
def get_data_for_create_order(get_exist_user_data, not_valid=False):
    data.ingredients["ingredients"] = Constants.TEST_ING_LIST
    url = urls.POST_GET_ORDER_ROUTE
    data.headers["Authorization"] = get_exist_user_data['response'].json()['accessToken']
    if not_valid is True:
        data.ingredients["ingredients"] = [f'new{Constants.TEST_BUN}']
    data.headers["Authorization"] = get_exist_user_data['response'].json()['accessToken']
    return {'url': url, 'data': data.ingredients, 'headers': data.headers}


@allure.step('Получение ответа на запрос')
def get_response_post_order(response):
    status_code = response.status_code
    resp_dict = {'status_code': status_code}
    if 200 <= status_code < 500:
        if 'success' in response.json():
            message_success = response.json()['success']
            resp_dict['message_success'] = message_success
        if 'order' in response.json():
            if 'owner' in response.json()['order']:
                owner_name = response.json()['order']['owner']['name']
                resp_dict['owner_name'] = owner_name
        if 'orders' in response.json():
            total = response.json()['total']
            resp_dict['total'] = total
        if 'message' in response.json():
            message = response.json()['message']
            resp_dict['message'] = message
    return resp_dict
