import pytest

from base_api.api_users import Users
from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import *
from helpers.sqlbd import SQLBD
from helpers.settings import Settings
import allure


def test_positive_users(auth_client):
    """Проверка получения конкретного пользователя."""
    with allure.step("Авторизация"):
        user = Users(auth_client(Settings.MOD_EMAIL, Settings.MOD_PASSWORD))
    with allure.step("Получение информации о пользователи"):
        response = user.get_user(Settings.ADMIN_NAME)
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 200)
    with allure.step("Валидация схемы"):
        RegisterSchema.model_validate(response.json())
    with allure.step("Проверка совпадения username"):
        assertions_fields(response, "username", Settings.ADMIN_NAME)

def test_get_user_not_found(auth_client):
    """Проверка поиска несуществуюшего пользователя"""
    with allure.step("Авторизация"):
        user = Users(auth_client(Settings.MOD_EMAIL, Settings.MOD_PASSWORD))
    with allure.step("Получение информации о пользователи"):
        name = "abracadabra"
        response = user.get_user(name)
    with allure.step("Статус код"):
        assertions_status_code(response, 404)
    with allure.step("Валидация схемы ответа"):
        SchemaUserNotFound.model_validate(response.json())
        assertions_fields(response, "detail", f"User '{name}' not found")
        assertions_fields(response, "error_code", "NOT_FOUND")
        assertions_fields(response, "status_code", 404)

def test_get_user_without_auth(auth_client):
    """Проверка поиска конкретного пользователя без авторизации"""
    with allure.step("Авторизация"):
        user = Users()
    with allure.step("Получение информации о пользователи"):
        response = user.get_user(Settings.ADMIN_NAME)
    with allure.step("Валидация ответа"):
        SchemanotAuth.model_validate(response.json())

def test_get_my_info(auth_client):
    """Проверка поиска собственного профиля"""
    with allure.step("Авторизация"):
        user = Users(auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD))
    with allure.step("Получение информации о пользователи"):
        response = user.get_user(Settings.ADMIN_NAME)
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 200)
    with allure.step("Валидация схемы"):
        RegisterSchema.model_validate(response.json())
    with allure.step("Проверка совпадения username"):
        assertions_fields(response, "username", Settings.ADMIN_NAME)

def test_get_ban_profile(auth_client):
    """Проверка поиска забаненного профиля"""
    with allure.step("Авторизация"):
        user = Users(auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD))
    with allure.step("Получение информации о пользователи"):
        response = user.get_user(Settings.BANNED_NAME)
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 200)
    with allure.step("Валидация схемы"):
        RegisterSchema.model_validate(response.json())

def test_get_ban_info(auth_client):
    """Проверка поиска забаненного профиля"""
    with allure.step("Авторизация"):
        user = Users(auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD))
    with allure.step("Получение информации о пользователи"):
        response = user.get_user(Settings.BANNED_NAME)
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 200)
    with allure.step("Валидация схемы"):
        RegisterSchema.model_validate(response.json())
    with allure.step("Проверка совпадения username"):
        assertions_fields(response, "username", Settings.BANNED_NAME)

def test_get_private_info(auth_client):
    """Проверка поиска приватного профиля"""
    with allure.step("Авторизация"):
        user = Users(auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD))
    with allure.step("Получение информации о пользователи"):
        response = user.get_user(Settings.PRIVATE_NAME)
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 200)
    with allure.step("Валидация схемы"):
        RegisterSchema.model_validate(response.json())
    with allure.step("Проверка совпадения username"):
        assertions_fields(response, "username", Settings.PRIVATE_NAME)
