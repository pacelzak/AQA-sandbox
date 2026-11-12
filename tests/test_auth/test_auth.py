import pytest

from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import *
from helpers.sqlbd import SQLBD
from helpers.settings import Settings
import allure


def test_positive_auth(create_user):
    """Проверка успешной авторизации зарегистрированного пользователя."""
    with allure.step("Авторизация"):
        api = Auth()
        response = api.login(create_user['email'], create_user['password'])
    with allure.step("Проверка статус кода"):
        assertions_status_code(response,200)
    with allure.step("Проверка схемы ответа"):
        LoginSchema.model_validate(response.json())

def test_login_without_register(create_data):
    with allure.step("Авторизация"):
        api = Auth()
        response = api.login(create_data['email'], create_data['password'])
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 401)
    with allure.step("Проверка схемы ответа"):
        FailedLoginSchema.model_validate(response.json())
    with allure.step("Валидация полей"):
        assertions_fields(response, "detail", "Invalid email or password")
        assertions_fields(response, "error_code", "UNAUTHORIZED")
        assertions_fields(response, "status_code", 401)

def test_login_with_wrong_password(create_user):
    """Проверка авторизации с неправильным паролем."""

    with allure.step("Авторизация с неправильным паролем"):
        api = Auth()
        response = api.login(create_user['email'],"WrongPassword123!" )
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 401)
    with allure.step("Проверка схемы ответа"):
        FailedLoginSchema.model_validate(response.json())
    with allure.step("Проверка полей ответа"):
        assertions_fields(response, "detail", "Invalid email or password")
        assertions_fields(response, "error_code", "UNAUTHORIZED")
        assertions_fields(response, "status_code", 401)

@pytest.mark.parametrize("email, password, expected_status",[("", None, 422), (None, "", 401),("", "", 422)])
def test_login_with_empty_fields(create_user, email, password, expected_status):
    """Проверка авторизации с пустыми полями."""
    email = email if email is not None else create_user["email"]
    password = password if password is not None else create_user["password"]
    with allure.step("Авторизация с неправильным паролем"):
        api = Auth()
        response = api.login(email, password)
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, expected_status)