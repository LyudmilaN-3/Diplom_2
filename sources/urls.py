import allure

MAIN_URL = 'https://stellarburgers.nomoreparties.site'


class UserAPIRoutes:

    ENDPOINT_USER_CREATE = '/api/auth/register'
    ENDPOINT_USER_LOGIN = '/api/auth/login'
    ENDPOINT_USER_UPDATE_DELETE = '/api/auth/user'

    @allure.step('Формирование эндпоинта')
    def post_reg_api_user_route(self):
        url = f'{MAIN_URL}{self.ENDPOINT_USER_CREATE}'
        return url

    @allure.step('Формирование эндпоинта')
    def post_login_api_user_route(self):
        url = f'{MAIN_URL}{self.ENDPOINT_USER_LOGIN}'
        return url

    def update_delete_api_user_route(self):
        url = f'{MAIN_URL}{self.ENDPOINT_USER_UPDATE_DELETE}'
        return url


class OrderAPIRoutes:

    ENDPOINT_ORDER_CREATE_GET = '/api/orders'

    @allure.step('Формирование эндпоинта')
    def post_get_api_order_route(self):
        url = f'{MAIN_URL}{self.ENDPOINT_ORDER_CREATE_GET}'
        return url
