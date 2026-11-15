from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import *
import allure

def test_positive_logout(create_user):
    """Проверка успешного выхода пользователя."""

    user = Auth()
    with allure.step("Авторизация пользователя"):
        login_response = user.login(
            create_user["email"],
            create_user["password"]
        )
        assertions_status_code(login_response, 200)
        access_token = login_response.json()["access_token"]
        refresh_token = login_response.json()["refresh_token"]
    with allure.step("Установка access token"):
        user.set_token(access_token)
    with allure.step("Выход пользователя"):
        response = user.logout(refresh_token)
    with allure.step("Проверка статус-кода"):
        assertions_status_code(response, 204)


def test_logout_without_refresh_token(create_user):
    """Пустой refresh_token."""

    user = Auth()
    with allure.step("Авторизация пользователя"):
        login_response = user.login(create_user["email"],create_user["password"])
        access_token = login_response.json()["access_token"]
        user.set_token(access_token)
    with allure.step("Запрос logout"):
        response = user.logout("")
    with allure.step("Проверка статус-кода"):
        assertions_status_code(response, 204)

def test_logout_none_refresh_token(create_user):
    """None refresh_token."""

    user = Auth()
    with allure.step("Авторизация пользователя"):
        login_response = user.login(create_user["email"],create_user["password"])
        access_token = login_response.json()["access_token"]
        user.set_token(access_token)
    with allure.step("Запрос logout"):
        response = user.logout(refresh_token=None)
    with allure.step("Проверка статус-кода"):
        assertions_status_code(response, 422)
    with allure.step("Валидация схемы"):
        HTTPValidationError.model_validate(response.json())

def test_logout_wrong_refresh_token(create_user):
    """None refresh_token."""

    user = Auth()
    with allure.step("Авторизация пользователя"):
        login_response = user.login(create_user["email"],create_user["password"])
        access_token = login_response.json()["access_token"]
        user.set_token(access_token)
    with allure.step("Запрос logout"):
        response = user.logout(access_token)
    with allure.step("Проверка статус-кода"):
        assertions_status_code(response, 204)

