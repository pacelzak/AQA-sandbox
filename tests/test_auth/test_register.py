import pytest

from base_api.api_auth import Auth
from helpers.assertions import *
from helpers.schema import *
from helpers.sqlbd import SQLBD
from helpers.settings import Settings
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

@pytest.mark.parametrize("email, username", [(Settings.ADMIN_EMAIL,None), (None, Settings.ADMIN_NAME), (Settings.ADMIN_EMAIL, Settings.ADMIN_NAME)])
def test_register_with_duplicate(email,username, create_data):

    """Регистрация с повторными данными"""
    with allure.step("Регистрация пользователя"):
        data_register = Auth()
        email = email or create_data["email"]
        username = username or create_data["username"]
        response = data_register.register(
            email=email,
            password=create_data["password"],
            display_name=create_data["display_name"],
            username=username
        )
    with allure.step("Проверка статуса ответа"):
        assertions_status_code(response, 409)
    with allure.step("Проверка полей"):
        assertions_fields(response, "detail", "User with this email or username already exists")
        assertions_fields(response, "error_code", "CONFLICT")
        RegisterDublicateSchema.model_validate(response.json())

@pytest.mark.parametrize("password, expected_status", [("A"*5, 422), ("A"*6, 201), ("A"*7, 201), ("A"*127, 201),("A"*128, 201), ("A"*129, 422), ("", 422)])
def test_validate_password(create_data, password, expected_status):
    """Успешная регистрация нового пользователя"""
    data_register = Auth()
    response = data_register.register(
        email=create_data["email"],
        password=password,
        display_name=create_data["display_name"],
        username=create_data['username']

    )
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, expected_status)

@pytest.mark.parametrize("display_name, expected_status", [("A"*0, 422), ("A"*1, 201), ("A"*99, 201), ("A"*100, 201),("A"*101, 422), ("", 422)])
def test_validate_password(create_data, display_name, expected_status):
    """Успешная регистрация нового пользователя"""
    data_register = Auth()
    response = data_register.register(
        email=create_data["email"],
        password=create_data["password"],
        display_name=display_name,
        username=create_data['username']

    )
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, expected_status)

@pytest.mark.parametrize("username, expected_status",     [
        # Проверка минимальной и максимальной длины
        ("A" * 2, 422),
        ("A" * 3, 201),
        ("A" * 30, 201),
        ("A" * 31, 422),
        ("", 422),

        # Проверка допустимых символов
        ("Test123", 201),
        ("Test_123", 201),
        ("Test-123", 422),
        ("Test@123", 422),
        ("Test!123", 422),
        ("Test 123", 422),
        ("Тест123", 422),
    ])
def test_validate_username(create_data, username, expected_status):

    data_register = Auth()
    response = data_register.register(
        email=create_data["email"],
        password=create_data["password"],
        display_name=create_data["display_name"],
        username=username

    )
    with allure.step("Проверка статус кода"):
        assertions_status_code(response, expected_status)

@pytest.mark.parametrize(
    "email, expected_status",
    [
        # Корректные форматы
        ("test@example.com", 201),
        ("test.user@example.com", 201),
        ("test_user@example.com", 201),
        ("test+tag@example.com", 201),

        # Отсутствует @
        ("testexample.com", 422),

        # Отсутствует локальная часть
        ("@example.com", 422),

        # Отсутствует домен
        ("test@", 422),

        # Некорректный домен
        ("test@example", 422),
        ("test@.com", 422),

        # Несколько символов @
        ("test@@example.com", 422),

        # Пробелы
        ("test user@example.com", 422),
        ("test@example .com", 422),

        # Некорректные точки
        (".test@example.com", 422),
        ("test.@example.com", 422),
        ("test..user@example.com", 422),

        ("", 422)
    ]
)
def test_validate_email(create_data, email, expected_status):
    auth = Auth()

    response = auth.register(
        email=email,
        password=create_data["password"],
        display_name=create_data["display_name"],
        username=create_data["username"]
    )

    with allure.step("Проверка статус-кода"):
        assertions_status_code(response, expected_status)