import pytest

from base_api.api_users import Users
from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import *
from helpers.sqlbd import SQLBD
from helpers.settings import Settings
import allure


def test_positive_list_user(auth_client):
    """Проверка получения списка пользователей."""
    with allure.step("Авторизация"):
        user = Users(auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD))
    with allure.step("Получение списка пользователей"):
        response = user.list_users()
    with allure.step("Проверка статус-кода"):
        assertions_status_code(response, 200)
    with allure.step("Валидация схемы ответа"):
        UserSchema.model_validate(response.json())
    data = response.json()
    with allure.step("Проверка параметров пагинации"):
        assert data["page"] == 1
        assert data["per_page"] == 20
        assert data["total"] >= 0
        assert data["pages"] >= 0
    with allure.step("Проверка количества пользователей"):
        assert len(data["items"]) <= data["per_page"]
    with allure.step("Проверка уникальности ID"):
        user_ids = [user["id"] for user in data["items"]]
        assert len(user_ids) == len(set(user_ids))

def test_positive_list_users_second_page(auth_client):
    """Проверка получения второй страницы пользователей."""

    user = Users(auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD))
    response = user.list_users(page=2, per_page=5)
    assertions_status_code(response, 200)
    data = response.json()
    assert data["page"] == 2
    assert data["per_page"] == 5
    assert len(data["items"]) == 2
    assert data["total"] == 7

def test_positive_list_users_unique_pages(auth_client):
    """Проверка отсутствия повторяющихся пользователей между страницами."""

    user = Users(auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD))
    first_page = user.list_users(page=1, per_page=5)
    second_page = user.list_users(page=2, per_page=5)
    assertions_status_code(first_page, 200)
    assertions_status_code(second_page, 200)
    first_ids = {item["id"] for item in first_page.json()["items"]}
    second_ids = {item["id"] for item in second_page.json()["items"]}
    assert first_ids.isdisjoint(second_ids)

def test_not_auth(auth_client):
    """Проверка запроса без токена."""

    user = Users()
    first_page = user.list_users()
    with allure.step("Статус код"):
        assertions_status_code(first_page, 403)
    with allure.step("Валидация ответа"):
        SchemanotAuth.model_validate(first_page.json())

