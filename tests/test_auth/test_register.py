from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import RegisterSchema
from helpers.sqlbd import SQLBD
import allure

def test_positive_register(create_data):

    """Успешная регистрация нового пользователя"""
    with allure.step("Регистрация нового пользователя"):
        data_register = Auth()
        response = data_register.register(
            email=create_data["email"],
            password=create_data["password"],
            display_name=create_data["display_name"],
            username=create_data["username"]
        )
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, 201)
    with allure.step("Проверка полей ожидаемому результату"):
        assertions_fields(response, "email", create_data["email"])
        assertions_fields(response, "username", create_data["username"])
        assertions_fields(response, "display_name", create_data["display_name"])
    with allure.step("Валидация ответа схеме"):
        response_data = response.json()
        RegisterSchema.model_validate(response_data)
    with allure.step("Проверка в бд"):
        bd = SQLBD()
        user = bd.info_user(response_data["id"])
        assertions_db_fields(user, "email", create_data["email"])
        assertions_db_fields(user, "username", create_data["username"])
        assertions_db_fields(user, "display_name", create_data["display_name"])