import pytest
from base_api.api_users import Users
from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import *
from helpers.sqlbd import SQLBD
from helpers.settings import Settings
import allure

def test_my_get_posts(auth_client):
    """Получения списка своих постов"""
    with allure.step('Авторизация'):
        cred = auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD)
        client = Users(cred)
        auth = Auth(cred)
    with allure.step("Получения списка постов"):
        my_username = auth.get_me().json()['username']
        id = auth.get_me().json()['id']
        response = client.get_user_post(username=my_username)
    with allure.step("Статус код"):
        assertions_status_code(response, 200)
    with allure.step('Валидация схемы'):
        GetUserPostSchema.model_validate(response.json())
    with allure.step("Проверяем количество постов"):
        sql = SQLBD()
        assert sql.count_posts(id) == len(response.json()["items"])


def test_friends_get_posts(auth_client):
    """Получения списка постов cвоих подписчиков"""
    with allure.step('Авторизация'):
        cred = auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD)
        client = Users(cred)
    with allure.step("Получения списка постов"):
        username = client.list_users().json()['items'][0]['username']
        id = client.list_users().json()['items'][0]['id']
        response = client.get_user_post(username=username)
    with allure.step("Статус код"):
        assertions_status_code(response, 200)
    with allure.step('Валидация схемы'):
        GetUserPostSchema.model_validate(response.json())
    with allure.step("Проверяем количество постов"):
        sql = SQLBD()
        assert sql.count_posts(id) == len(response.json()["items"])

def test_unsucribe_get_posts(auth_client):
    """Получения списка постов cвоих подписчиков"""
    with allure.step('Авторизация'):
        cred = auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD)
        client = Users(cred)
    with allure.step("Получения списка постов"):
        username = client.get_suggestions().json()[0]['username']
        id = client.get_suggestions().json()[0]['id']
        response = client.get_user_post(username=username)
    with allure.step("Статус код"):
        assertions_status_code(response, 200)
    with allure.step('Валидация схемы'):
        GetUserPostSchema.model_validate(response.json())
    with allure.step("Проверяем количество постов"):
        sql = SQLBD()
        assert sql.count_posts(id) == len(response.json()["items"])

def test_negative_get_posts(auth_client):
    """Получения списка постов несуществующего пользоватедя"""
    with allure.step('Авторизация'):
        cred = auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD)
        client = Users(cred)
    with allure.step("Получения списка постов"):
        username = client.get_suggestions().json()[0]['username']
        id = client.get_suggestions().json()[0]['id']
        response = client.get_user_post(username=username+'s')
    with allure.step("Статус код"):
        assertions_status_code(response, 404)
    with allure.step("Валидация ответа"):
        SchemaUserNotFound.model_validate(response.json())

def test_private_get_posts(auth_client):
    """Получения списка постов приватного пользоватедя"""
    with allure.step('Авторизация'):
        cred = auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD)
        client = Users(cred)
    with allure.step("Получения списка постов"):
        response = client.get_user_post(username=Settings.PRIVATE_NAME)
    with allure.step("Статус код"):
        assertions_status_code(response, 200)

def test_private_get_posts(auth_client):
    """Получения списка постов забанненого пользоватедя"""
    with allure.step('Авторизация'):
        cred = auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD)
        client = Users(cred)
    with allure.step("Получения списка постов"):
        response = client.get_user_post(username=Settings.BANNED_NAME)
    with allure.step("Статус код"):
        assertions_status_code(response, 200)



