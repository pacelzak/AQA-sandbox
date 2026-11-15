
from helpers.schema import RegisterSchema
from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.settings import Settings
import allure


def test_positive_get_me(auth_client):
    """Информация о своем аккаунте"""
    with allure.step("Авторизация"):
        client = Auth(client=auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD))
    with allure.step("Информация о аккаунте"):
        info = client.get_me()
    with allure.step("Проверка статус кода"):
        assertions_status_code(info, 200)
    with allure.step("Валидация схемы"):
        RegisterSchema.model_validate(info.json())
    with allure.step("Проверка полей"):
        assertions_fields(info, 'email', Settings.ADMIN_EMAIL)

def test_get_me_without_auth():
    """Информация о аккаунте без авторизации"""
    with allure.step('Авторизаци'):
        client = Auth()
    with allure.step("Информация о аккаунте"):
        info = client.get_me()
    with allure.step("Проверка статус кода"):
        assertions_status_code(info, 403)
