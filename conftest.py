import pytest

from sources.user_support import get_data_for_create_user, delete_user, register_new_user


@pytest.fixture
def get_new_user_data():
    payload = get_data_for_create_user()
    return payload


@pytest.fixture
def get_exist_user_data():
    payload = get_data_for_create_user()
    response = register_new_user(payload)
    return {'payload': payload, 'response': response}


@pytest.fixture
def delete_fix():
    token = {}
    yield token
    delete_user(token)
