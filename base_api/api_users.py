from base_api.api import BaseAPI


class Users(BaseAPI):

    def list_users(self, search=None, sort_by=None, sort_order=None, page=None, per_page=None):
        """
        Получает список пользователей с возможностью поиска, сортировки и пагинации.

        Args:
            search: Строка для поиска пользователей.
            sort_by: Поле сортировки (created_at, username, display_name).
            sort_order: Направление сортировки (asc или desc).
            page: Номер страницы.
            per_page: Количество пользователей на странице.

        Returns:
            httpx.Response: Ответ API со списком пользователей.
        """
        params = {
            "search": search,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "page": page,
            "per_page": per_page
        }

        return self.get("/api/users", params=params)

    def get_suggestions(self):
        """
        Получает до 5 наиболее активных пользователей, на которых
        текущий пользователь ещё не подписан.

        Returns:
            httpx.Response: Ответ API со списком рекомендаций.
        """
        return self.get("/api/users/suggestions")

    def get_user(self, username=None):
        """
        Получает информацию о пользователе по его username.

        Args:
            username: Уникальное имя пользователя.

        Returns:
            httpx.Response: Ответ API с информацией о пользователе.
        """
        return self.get(f"/api/users/{username}")

    def update_me(self, **kwargs):
        """
        Обновляет профиль текущего авторизованного пользователя.

        Args:
            **kwargs: Поля профиля для обновления (display_name, bio, is_private).

        Returns:
            httpx.Response: Ответ API с обновлённой информацией профиля.
        """
        return self.patch("/api/users/me", json=kwargs)

    def update_avatar(self, file):
        """
        Загружает аватар текущего авторизованного пользователя.

        Args:
            file: Путь к файлу изображения.

        Returns:
            httpx.Response: Ответ API с обновлённой информацией профиля.
        """
        with open(f"{file}", 'rb') as img:
            files = {'file': ('my_photo.jpg', img, 'image/jpeg')}
            return self.post('/api/users/me/avatar', files=files)

    def delete_avatar(self):
        """
        Удаляет аватар текущего авторизованного пользователя.

        Returns:
            httpx.Response: Ответ API после удаления аватара.
        """
        return self.delete("/api/users/me/avatar")

    def get_user_post(self, username=None, page=None, per_page=None):
        """
        Получает список постов указанного пользователя с пагинацией.

        Args:
            username: Имя пользователя, чьи посты необходимо получить.
            page: Номер страницы.
            per_page: Количество постов на странице.

        Returns:
            httpx.Response: Ответ API со списком постов пользователя.
        """
        params = {"page": page, "per_page": per_page}
        return self.get(f"/api/users/{username}/posts", params=params)

    def get_followers(self, username=None, page=None, per_page=None):
        """
        Получает список подписчиков указанного пользователя.

        Args:
            username: Имя пользователя, подписчиков которого необходимо получить.
            page: Номер страницы.
            per_page: Количество подписчиков на странице.

        Returns:
            httpx.Response: Ответ API со списком подписчиков.
        """
        params = {"page": page, "per_page": per_page}
        return self.get(f"/api/users/{username}/followers", params=params)

    def get_following(self, username=None, page=None, per_page=None):
        """
        Получает список пользователей, на которых подписан указанный пользователь.

        Args:
            username: Имя пользователя, список подписок которого необходимо получить.
            page: Номер страницы.
            per_page: Количество подписок на странице.

        Returns:
            httpx.Response: Ответ API со списком подписок.
        """
        params = {"page": page, "per_page": per_page}
        return self.get(f"/api/users/{username}/following", params=params)