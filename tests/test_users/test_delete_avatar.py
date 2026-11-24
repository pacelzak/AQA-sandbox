
from base_api.api_users import Users
from base_api.api_auth import Auth
from helpers.assertions import *
import allure
from pathlib import Path

TEST_DATA = Path(__file__).resolve().parents[2] / "test_data"
AVATAR_PATH = TEST_DATA / "ex.jpg"

def test_positive_delete_avatar_when_avatar_is_absent(auth_client, create_user):
    """Удаление аватара которого нет"""
    with allure.step("Авторизация"):
        client = auth_client(create_user["email"], create_user["password"])
        session = Users(client)
        auth = Auth(client)
    with allure.step("Удаление фото"):
        response = session.delete_avatar()
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 204)
    with allure.step("Проверям что аватар удалился"):
        new_avatar = auth.get_me()
        assert new_avatar.json()["avatar_url"] is None

def test_change_avatar(auth_client,create_user):
    """Удаление существуюшего аватара"""
    with allure.step("Авторизация"):
        client = auth_client(create_user["email"], create_user["password"])
        session = Users(client)
        auth = Auth(client)
    with allure.step("Проверям старый аватр"):
        upload_avatar = session.update_avatar(AVATAR_PATH)
        old_avatar = auth.get_me().json()["avatar_url"]
        assert old_avatar is not None
    with allure.step("Удаление фото"):
        response = session.delete_avatar()
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 204)
    with allure.step("Проверям что аватар удалился"):
        new_avatar = auth.get_me()
        assert new_avatar.json()["avatar_url"] is None