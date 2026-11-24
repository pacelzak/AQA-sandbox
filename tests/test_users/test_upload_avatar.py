import pytest
from base_api.api_users import Users
from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import *
from helpers.sqlbd import SQLBD
from helpers.settings import Settings
import allure

from pathlib import Path

TEST_DATA = Path(__file__).resolve().parents[2] / "test_data"
AVATAR_PATH = TEST_DATA / "ex.jpg"

def test_positive_upload_avatar(auth_client,create_user):
    """Загрузка аватара"""
    with allure.step("Авторизация"):
        client = auth_client(create_user["email"], create_user["password"])
        session = Users(client)
        auth = Auth(client)
    with allure.step("Проверям что аватор пустой"):
        old_avatar = auth.get_me().json()["avatar_url"]
    with allure.step("Загрузка фото"):
        response = session.update_avatar(AVATAR_PATH)
        new_avatar = response.json()["avatar_url"]
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 200)
    with allure.step("Валидация схемы"):
        RegisterSchema.model_validate(response.json())
        assert new_avatar
    with allure.step("Проверям что аватар изменился"):
        assert new_avatar != old_avatar
        profile = auth.get_me()
        assertions_status_code(profile, 200)
        assert profile.json()["avatar_url"] == new_avatar



