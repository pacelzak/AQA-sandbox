from base_api.api import BaseAPI
from base_api.api_auth import Auth
from helpers.data_generation import DataGenerator
from helpers.settings import Settings
import pytest
import httpx


@pytest.fixture()
def get_token():
    def auth(email: str, password: str) -> str:
        authorization = Auth()
        response = authorization.login(email, password)
        return response.json()["access_token"]
    return auth

@pytest.fixture()
def set_token():
    def install_token(token: str):
        api = BaseAPI()
        api.set_token(token)
        return api.client
    return install_token

@pytest.fixture()
def auth_client(get_token, set_token):
    def creds(email: str, password: str) -> str:
        token = get_token(email, password)
        return set_token(token)
    return creds

@pytest.fixture()
def create_data():
    data = DataGenerator()
    return {
        'email': data.email,
        'username': data.username,
        'password': data.password,
        'display_name': data.display_name}


@pytest.fixture(autouse=True)
def reset_database():
    """Обнуление базы данных"""
    yield
    return httpx.post(Settings.RESET_URL)

@pytest.fixture()
def create_user(create_data):
    api = Auth()
    response = api.register(create_data['email'],  create_data['username'], create_data['password'], create_data['display_name'])
    assert response.status_code == 201, response.text
    return create_data




