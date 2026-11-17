import pytest
from base_api.api_users import Users
from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import *
from helpers.sqlbd import SQLBD
from helpers.settings import Settings
import allure

def test_positive_get_suggestions(auth_client):
    with allure.step("Авторизация"):
        user = Users(auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD))
    with allure.step("Получение 5 пользователей"):
        response = user.get_suggestions()
    with allure.step("Статус код"):
        assertions_status_code(response, 200)
    with allure.step("Валидация схемы ответа"):
        Suggestions.model_validate(response.json())
    with allure.step("Проверка, что получили не больше 5 пользователей"):
        list_id = []
        for  key in response.json():
            list_id.append(key["id"])
        assert len(list_id) <= 5

