import pytest
from base_api.api_users import Users
from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import *
from helpers.sqlbd import SQLBD
from helpers.settings import Settings
import allure


def test_count_new_users(auth_client, create_user):
    """Количество подписчиков у только созданного аккунта"""
    with allure.step('Авторизация'):
        session = auth_client(create_user["email"], create_user["password"])
        client = Users(session)
        auth = Auth(session)
        id = auth.get_me().json()["id"]
    with allure.step("Проверяем количество подписчиков"):
        response = client.get_followers(create_user["username"])
    with allure.step("Статус код"):
        assertions_status_code(response, 200)
    with allure.step("Валидация схемы"):
        RootsFollowersSchema.model_validate(response.json())
    with allure.step("Количество подписчиков"):
        assert len(response.json()["items"]) == 0
    with allure.step("Количество подписчиков в БД"):
        sql = SQLBD()
        assert sql.count_followers("following_id", id) == 0

def test_count_users(auth_client, create_user):
    """Количество подписчиков у аккаунта"""

    with allure.step('Авторизация'):
        client = Users(auth_client(create_user["email"], create_user["password"]))
    with allure.step("Получаем список подписчиков"):
        response = client.get_followers(Settings.ADMIN_NAME)
    with allure.step("Статус код"):
        assertions_status_code(response, 200)
    with allure.step("Валидация схемы"):
        result = RootsFollowersSchema.model_validate(response.json())
    with allure.step("Количество подписчиков в БД и API"):
        sql = SQLBD()
        user_id = client.get_user(Settings.ADMIN_NAME).json()["id"]
        db_count = sql.count_followers("following_id", user_id)
        assert db_count == result.total

def test_count_incorrect_users(auth_client, create_user):
    """Неверный username"""
    with allure.step('Авторизация'):
        client = Users(auth_client(create_user["email"], create_user["password"]))
    with allure.step("Проверяем количество подписчиков"):
        username = create_user["username"]+"s"
        response = client.get_followers(username)
    with allure.step("Статус код"):
        assertions_status_code(response, 404)
    with allure.step("Валидация схемы"):
        SchemaUserNotFound.model_validate(response.json())
        assertions_fields(response, "detail", f"User '{username}' not found")
        assertions_fields(response, "error_code", "NOT_FOUND")
        assertions_fields(response, "status_code", 404)






