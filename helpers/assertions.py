

def assertions_status_code(response, expected_status_code):
    """Проверяет соответствие HTTP-статуса ожидаемому.

     Args:
         response: ответ от сервера
         expected_status_code: ожидаемый статус код """

    actual_status_code = response.status_code

    assert actual_status_code == expected_status_code, (
        f"Ожидался статус-код {expected_status_code}, "
        f"получен {actual_status_code}. "
        f"Ответ сервера: {response.text}"
    )

def assertions_fields(response, fields, expected_fields):
    """Проверяет соответствие ожидаемого значения поля фактическому.

     Args:
         response: ответ от сервера
         fields: поля для проверки
         expected_fields: ожидаемое значения для fields"""

    actual_value = response.json()[fields]
    assert actual_value == expected_fields, (
        f"Поле '{fields}': ожидалось значение {expected_fields}, "
        f"получено {actual_value}."
    )

def assertions_db_fields(user, field, expected_value):
    actual_value = user._mapping[field]

    assert actual_value == expected_value, (
        f"Поле '{field}': ожидалось '{expected_value}', "
        f"получено '{actual_value}'."
    )