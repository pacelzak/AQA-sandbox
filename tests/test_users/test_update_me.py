import pytest
from base_api.api_users import Users
from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import *
from helpers.data_generation import DataGenerator
from helpers.settings import Settings
import allure


def test_positive_update_me_display_name(auth_client,create_data):
        """Изменения display_name"""
        with allure.step("Авторизация"):
            client = auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD)
            user = Users(client)
            auth = Auth(client)
        with allure.step("Получаем текущий профиль"):
            info_user = auth.get_me()
            old_display_name = info_user.json()["display_name"]
        with allure.step("Обновляем display_name"):
            new_display_name = create_data["display_name"]
            changed_display_name = user.update_me(display_name=new_display_name)
        with allure.step("Статус код ответа"):
            assertions_status_code(changed_display_name, 200)
        with allure.step("Проверка изменения имени"):
            assert old_display_name != new_display_name
            display_name_after_change = auth.get_me().json()["display_name"]
            assert display_name_after_change == new_display_name
        with allure.step("Валидация схемы"):
            RegisterSchema.model_validate(changed_display_name.json())

@pytest.mark.parametrize("display_name_length", [1,99,100])
def test_positive_validate_update_display_name(auth_client,display_name_length):
    """Позитивная валидация display_name"""
    with allure.step("Авторизация"):
        client = auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD)
        user = Users(client)
        auth = Auth(client)
    with allure.step("Получаем текущий профиль"):
        info_user = auth.get_me()
        old_display_name = info_user.json()["display_name"]
    with allure.step("Обновляем display_name"):
        faker = DataGenerator()
        new_display_name = faker.make_display_name(display_name_length)
        changed_display_name = user.update_me(display_name=new_display_name)
    with allure.step("Проверка не совпадений имени"):
        assert old_display_name != new_display_name
    with allure.step("Проверка статус кода"):
        assertions_status_code(changed_display_name,200)


def test_update_bio(auth_client):
    """Обновления bio"""
    with allure.step("Авторизация"):
        client = auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD)
        user = Users(client)
        auth = Auth(client)
    with allure.step("Получаем текущий bio"):
        info_user = auth.get_me()
        old_bio = info_user.json()["bio"]
    with allure.step("Обновляем bip"):
        faker = DataGenerator()
        changed_bio = user.update_me(bio=faker.make_bio())
    with allure.step("Статус код ответа"):
        assertions_status_code(changed_bio, 200)
    with allure.step("Проверка изменения имени"):
        assert old_bio != changed_bio
    with allure.step("Валидация схемы"):
        RegisterSchema.model_validate(changed_bio.json())


@pytest.mark.parametrize("len_bio", [0,1,499,500])
def test_positive_validate_update_bio(auth_client,len_bio):
    """Позитивная валидация bio"""
    with allure.step("Авторизация"):
        client = auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD)
        user = Users(client)
        auth = Auth(client)
    with allure.step("Получаем текущий профиль"):
        info_user = auth.get_me()
        old_bio = info_user.json()["display_name"]
    with allure.step("Обновляем display_name"):
        faker = DataGenerator()
        if len_bio == 0:
            new_bio = ''
        else:
            new_bio = faker.make_display_name(len_bio)
        changed_bio = user.update_me(bio=new_bio)
    with allure.step("Проверка не совпадений имени"):
        assert old_bio != new_bio
    with allure.step("Проверка статус кода"):
        assertions_status_code(changed_bio,200)


@pytest.mark.parametrize("len_bio", [501,502])
def test_negative_validate_update_bio(auth_client,len_bio):
    """Негативная валидация bio"""
    with allure.step("Авторизация"):
        client = auth_client(Settings.ADMIN_EMAIL, Settings.ADMIN_PASSWORD)
        user = Users(client)
        auth = Auth(client)
    with allure.step("Получаем текущий профиль"):
        info_user = auth.get_me()
        old_bio = info_user.json()["display_name"]
    with allure.step("Обновляем display_name"):
        faker = DataGenerator()
        new_bio = faker.make_display_name(len_bio)
        changed_bio = user.update_me(bio=new_bio)
    with allure.step("Проверка не совпадений имени"):
        assert old_bio != new_bio
    with allure.step("Проверка статус кода"):
        assertions_status_code(changed_bio,422)








