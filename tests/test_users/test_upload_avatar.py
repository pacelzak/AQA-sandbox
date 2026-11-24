import pytest
from base_api.api_users import Users
from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import *
import allure

from pathlib import Path

TEST_DATA = Path(__file__).resolve().parents[2] / "test_data"
AVATAR_PATH = TEST_DATA / "ex.jpg"
NEW_AVATAR_PATH = TEST_DATA / "avatar.jpg"
FILE_PATH = TEST_DATA / "file.txt"
PDF_PATH = TEST_DATA / "ex.pdf"


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


def test_change_avatar(auth_client,create_user):
    """Загрузка нового аватара"""
    with allure.step("Авторизация"):
        client = auth_client(create_user["email"], create_user["password"])
        session = Users(client)
        auth = Auth(client)
    with allure.step("Проверям старый аватр"):
        upload_avatar = session.update_avatar(AVATAR_PATH)
        old_avatar = auth.get_me().json()["avatar_url"]
        assert old_avatar is not None
    with allure.step("Загрузка фото"):
        response = session.update_avatar(NEW_AVATAR_PATH)
        new_avatar = response.json()["avatar_url"]
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 200)
    with allure.step("Проверям что аватар изменился"):
        assert new_avatar != old_avatar
        profile = auth.get_me()
        assertions_status_code(profile, 200)
        assert profile.json()["avatar_url"] == new_avatar

@pytest.mark.parametrize("file", [FILE_PATH, PDF_PATH])
def test_failed_upload_avatar(auth_client,create_user, file):
    """Загрузка аватара"""
    with allure.step("Авторизация"):
        client = auth_client(create_user["email"], create_user["password"])
        session = Users(client)
    with allure.step("Загрузка файла"):
        response = session.update_avatar(file)
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 400)
    with allure.step("Валидация схемы ответа"):
        RegisterDublicateSchema.model_validate(response.json())
    with allure.step("Провера полей"):
        assertions_fields(response,"detail","Only JPEG, PNG, GIF, WebP images are allowed")
        assertions_fields(response, "error_code", "BAD_REQUEST")
        assertions_fields(response, "status_code", 400)

def test_failed_upload_does_not_change_avatar(auth_client, create_user):
    """Неудачная загрузка не должна менять существующий аватар."""
    with allure.step("Авторизация"):
        client = auth_client(create_user["email"], create_user["password"])
        session = Users(client)
        auth = Auth(client)
    with allure.step("Загрузка первоначального аватара"):
        upload = session.update_avatar(AVATAR_PATH)
        assertions_status_code(upload, 200)
    with allure.step("Получение URL текущего аватара"):
        profile = auth.get_me()
        assertions_status_code(profile, 200)
        old_avatar = profile.json()["avatar_url"]
        assert old_avatar is not None
    with allure.step("Попытка загрузки неподдерживаемого файла"):
        response = session.update_avatar(PDF_PATH)
        assertions_status_code(response, 400)
    with allure.step("Проверка, что аватар не изменился"):
        profile = auth.get_me()
        assertions_status_code(profile, 200)
        new_avatar = profile.json()["avatar_url"]
        assert new_avatar == old_avatar

