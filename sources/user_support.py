import allure
import requests
import random
import string

from sources import data, urls


@allure.step('Формирование тела запроса для регистрации пользователя')
def get_data_for_create_user():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string
    email = f'{generate_random_string(5)}@gmail.com'
    password = generate_random_string(10)
    name = generate_random_string(10)
    payload = {
        'email': email,
        'password': password,
        'name': name
    }
    return payload


@allure.step('Регистрация нового пользователя')
def register_new_user(get_new_user_data, miss_field=None):
    url = urls.POST_REG_USER_ROUTE
    if miss_field is not None:
        payload = get_invalid_new_user_data(miss_field)
        return requests.post(url=url, data=payload)
    payload = get_new_user_data
    return requests.post(url=url, data=payload)


@allure.step('Логин существующего пользователя')
def login_exist_user(get_exist_user_data, wrong_field=None):
    url = urls.POST_LOGIN_USER_ROUTE
    if wrong_field is not None:
        payload = get_invalid_new_user_data(wrong_field)
        return requests.post(url=url, data=payload)
    payload = get_exist_user_data
    return requests.post(url=url, data=payload)


@allure.step('Изменение данных пользователя')
def update_exist_user(get_exist_user_data, not_auth, update_field=None):
    url = urls.UPDATE_DELETE_USER_ROUTE
    payload = get_update_new_user_data(get_exist_user_data, update_field)
    if not_auth is True:
        return requests.patch(url=url, data=payload)
    data.headers["Authorization"] = get_exist_user_data['response'].json()['accessToken']
    return requests.patch(url=url, data=payload, headers=data.headers)


@allure.step('Получение ответа на запрос')
def get_response_post_user(response):
    status_code = response.status_code
    message_success = response.json()['success']
    resp_dict = {
        'status_code': status_code,
        'message_success': message_success,
    }
    if 'user' in response.json():
        user_email = response.json()['user']['email']
        user_name = response.json()['user']['name']
        resp_dict['email'] = user_email
        resp_dict['name'] = user_name
    if 'message' in response.json():
        message = response.json()['message']
        resp_dict['message'] = message
    if 'accessToken' in response.json():
        access_token = response.json()['accessToken']
        resp_dict['access_token'] = access_token
    return resp_dict


@allure.step('Удаление пользователя')
def delete_user(token):
    if 'access_token' in token:
        url = urls.UPDATE_DELETE_USER_ROUTE
        data.headers["Authorization"] = token['access_token']
        requests.delete(url=url, headers=data.headers)
    elif 'token' in token:
        url = urls.UPDATE_DELETE_USER_ROUTE
        data.headers["Authorization"] = token['token']['accessToken']
        requests.delete(url=url, headers=data.headers)


@allure.step('Формирование тела запроса с незаполненным обязательным полем')
def get_invalid_new_user_data(miss_field):
    payload = get_data_for_create_user()
    if miss_field == 'email':
        payload.pop('email')
    if miss_field == 'password':
        payload.pop('password')
    if miss_field == 'name':
        payload.pop('name')
    return payload


@allure.step('Формирование тела запроса с неверным обязательным полем')
def get_invalid_exist_user_data(get_exist_user_data, wrong_field):
    payload = get_exist_user_data['payload']
    if wrong_field == 'email':
        payload['email'] = f'new{get_exist_user_data["email"]}'
    if wrong_field == 'password':
        payload['password'] = f'new{get_exist_user_data["password"]}'
    return payload


@allure.step('Формирование тела запроса с изменённым обязательным полем')
def get_update_new_user_data(get_exist_user_data, update_field):
    payload = get_exist_user_data['payload']
    if update_field == 'email':
        payload['email'] = f'new{payload["email"]}'
    if update_field == 'name':
        payload['name'] = f'new{payload["name"]}'
    return payload
