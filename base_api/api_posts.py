import httpx
from uuid import UUID
from base_api.api import BaseAPI


class Posts(BaseAPI):
    """Клиент для работы с публикациями: создание, получение, удаление и управление публикациями."""

    def get_list_post(self, author_id: UUID) -> httpx.Response:
        """
        Получает список публикаций.

        :param author_id: UUID автора публикаций.
        :return: Ответ API со списком публикаций.
        """
        return self.get("/api/posts")

    def post_create_post(self, content: str, image_url: str | None = None) -> httpx.Response:
        """
        Создаёт новую публикацию.

        :param content: Текст публикации.
        :param image_url: URL изображения публикации (необязательный параметр).
        :return: Ответ API с созданной публикацией.
        """
        payload = {
            "content": content,
            "image_url": image_url,
            "visibility": "public"
        }

        return self.post("/api/posts", json=payload)

    def get_feed(self) -> httpx.Response:
        """
        Получает ленту публикаций авторизованного пользователя.

        :return: Ответ API с лентой публикаций.
        """
        return self.get("/api/posts/feed")

    def get_post(self, post_id: UUID) -> httpx.Response:
        """
        Получает публикацию по её идентификатору.

        :param post_id: UUID публикации.
        :return: Ответ API с данными публикации.
        """
        return self.get(f"/api/posts/{post_id}")

    def patch_post(self, post_id: UUID, content: str) -> httpx.Response:
        """
        Обновляет текст публикации.

        :param post_id: UUID публикации.
        :param content: Новый текст публикации.
        :return: Ответ API с обновлённой публикацией.
        """
        return self.patch(f"/api/posts/{post_id}", json={"content": content})

    def delete_post(self, post_id: UUID, reason: str | None = None) -> httpx.Response:
        """
        Удаляет публикацию.

        :param post_id: UUID публикации.
        :param reason: Причина удаления (необязательный параметр).
        :return: Ответ API об удалении публикации.
        """
        params = {"reason": reason} if reason is not None else None
        return self.delete(f"/api/posts/{post_id}", params=params)

    def post_repost(self, post_id: UUID, repost_type: str = "repost",
                    content: str | None = None) -> httpx.Response:
        """
        Создаёт репост публикации.

        :param post_id: UUID исходной публикации.
        :param repost_type: Тип репоста (repost или quote).
        :param content: Текст комментария к репосту (необязательный параметр).
        :return: Ответ API с созданным репостом.
        """
        payload = {
            "repost_type": repost_type,
            "content": content
        }
        return self.post(f"/api/posts/{post_id}/repost", json=payload)

    def pin_post(self, post_id: UUID) -> httpx.Response:
        """
        Закрепляет публикацию в профиле.

        :param post_id: UUID публикации.
        :return: Ответ API о результате закрепления.
        """
        return self.post(f"/api/posts/{post_id}/pin")

    def delete_unpin_post(self, post_id: UUID) -> httpx.Response:
        """
        Открепляет публикацию в профиле.

        :param post_id: UUID публикации.
        :return: Ответ API о результате открепления.
        """
        return self.delete(f"/api/posts/{post_id}/pin")

