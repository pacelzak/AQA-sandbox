import httpx
from uuid import UUID
from base_api.api import BaseAPI


class Bookmarks(BaseAPI):
    """Клиент для работы с закладками публикаций."""

    def get_list_bookmarks(self) -> httpx.Response:
        """
        Получает список закладок авторизованного пользователя.

        :return: Ответ API со списком сохранённых публикаций.
        """
        return self.get("/api/bookmarks")

    def post_bookmarks_post(self, post_id: UUID) -> httpx.Response:
        """
        Добавляет публикацию в закладки.

        :param post_id: UUID публикации.
        :return: Ответ API с результатом добавления публикации в закладки.
        """
        return self.post(f"/api/posts/{post_id}/bookmark")

    def delete_unbookmarks_post(self, post_id: UUID) -> httpx.Response:
        """
        Удаляет публикацию из закладок.

        :param post_id: UUID публикации.
        :return: Ответ API с результатом удаления публикации из закладок.
        """
        return self.delete(f"/api/posts/{post_id}/bookmark")