import httpx
from base_api.api import BaseAPI


class Auth(BaseAPI):
    """Клиент для группы эндпоинтов /api/auth (регистрация, вход, токены, профиль)."""

    def register(
        self,
        email: str,
        username: str,
        password: str,
        display_name: str,
    ) -> httpx.Response:
        """Регистрирует нового пользователя.

        POST /api/auth/register

        Args:
            email: email пользователя.
            username: имя пользователя, 3-30 символов (буквы, цифры, "_").
            password: пароль, 6-128 символов.
            display_name: отображаемое имя, 1-100 символов.

        Returns:
            201 с данными пользователя или 422 при ошибке валидации.
        """
        payload = {
            "email": email,
            "username": username,
            "password": password,
            "display_name": display_name,
        }
        return self.post("/api/auth/register", json=payload)

    def login(self, email: str, password: str) -> httpx.Response:
        """Выполняет вход по email и паролю.

        POST /api/auth/login

        Args:
            email: email пользователя.
            password: пароль пользователя.

        Returns:
            200 с `access_token` и `refresh_token` или ошибка (422 при невалидных данных).
            Токен автоматически не сохраняется: для авторизованных запросов
            передайте `access_token` в `set_token()`.
        """
        payload = {"email": email, "password": password}
        return self.post("/api/auth/login", json=payload)

    def refresh(self, refresh_token: str) -> httpx.Response:
        """Обновляет пару токенов по refresh-токену.

        POST /api/auth/refresh

        Args:
            refresh_token: refresh-токен, полученный при логине.

        Returns:
            200 с новой парой токенов или ошибка (422 при невалидных данных).
        """
        payload = {"refresh_token": refresh_token}
        return self.post("/api/auth/refresh", json=payload)

    def logout(self, refresh_token: str) -> httpx.Response:
        """Завершает сессию, делая refresh-токен недействительным.

        POST /api/auth/logout (требует авторизации: сначала вызовите `set_token()`).

        Args:
            refresh_token: refresh-токен текущей сессии.

        Returns:
            204 без тела при успехе или ошибка (422 при невалидных данных).
        """
        payload = {"refresh_token": refresh_token}
        return self.post("/api/auth/logout", json=payload)

    def get_me(self) -> httpx.Response:
        """Возвращает профиль текущего авторизованного пользователя.

        GET /api/auth/me (требует авторизации: сначала вызовите `set_token()`).

        Returns:
            200 с данными пользователя.
        """
        return self.get("/api/auth/me")