import pytest
import time

from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import *
from helpers.sqlbd import SQLBD
from helpers.settings import Settings
import allure

def test_positive_refresh_token(create_user):
    """Обновление токена"""
    with allure.step("Создания пользователя и авторизация"):
        user = Auth()
        login_user = user.login(create_user["email"], create_user["password"])
        old_refresh = login_user.json()["refresh_token"]
        old_token = login_user.json()["access_token"]
        user.set_token(old_token)
    with allure.step("Обновления токена"):
        time.sleep(0.9)
        response = user.refresh(old_refresh)
        new_refresh = response.json()["refresh_token"]
        new_token = response.json()["access_token"]
    with allure.step("Статус код"):
        assertions_status_code(response, 200)
    with allure.step("Проверка различий старого и нового токена"):
        assert old_refresh != new_refresh
        assert old_token != new_token
    with allure.step("Валидация схемы"):
        LoginSchema.model_validate(response.json())


def test_refresh_with_empty_token(create_user):
    """Проверка обновления токена с пустым refresh_token."""

    with allure.step("Создания пользователя и авторизация"):
        user = Auth()
        login_user = user.login(create_user["email"], create_user["password"])
        old_token = login_user.json()["access_token"]
        user.set_token(old_token)
    with allure.step("Обновления токена"):
        time.sleep(0.9)
        response = user.refresh("")
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 401)
    with allure.step("Проверка валидации ответа"):
        FailedLoginSchema.model_validate(response.json())

def test_refresh_with_none_token(create_user):
    """Не передаем refresh_token."""

    with allure.step("Создания пользователя и авторизация"):
        user = Auth()
        login_user = user.login(create_user["email"], create_user["password"])
        old_token = login_user.json()["access_token"]
        user.set_token(old_token)
    with allure.step("Обновления токена"):
        time.sleep(0.9)
        response = user.refresh(None)
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 422)
    with allure.step("Проверка валидации ответа"):
        HTTPValidationError.model_validate(response.json())

def test_refresh_with_none_token(create_user):
    """Неерный refresh_token."""

    with allure.step("Создания пользователя и авторизация"):
        user = Auth()
        login_user = user.login(create_user["email"], create_user["password"])
        old_token = login_user.json()["access_token"]
        user.set_token(old_token)
    with allure.step("Обновления токена"):
        time.sleep(0.9)
        response = user.refresh(old_token)
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 401)
    with allure.step("Проверка валидации ответа"):
        FailedLoginSchema.model_validate(response.json())