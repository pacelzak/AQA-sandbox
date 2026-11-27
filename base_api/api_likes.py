import httpx
from uuid import UUID
from base_api.api import BaseAPI


class Likes(BaseAPI):
    """Клиент для управления лайками публикаций и комментариев."""

    def post_like_post(self, post_id: UUID) -> httpx.Response:
        """
        Ставит лайк публикации.

        :param post_id: UUID публикации.
        :return: Ответ API с результатом добавления лайка.
        """
        return self.post(f"/api/posts/{post_id}/like")

    def delete_unlike_post(self, post_id: UUID) -> httpx.Response:
        """
        Удаляет лайк с публикации.

        :param post_id: UUID публикации.
        :return: Ответ API с результатом удаления лайка.
        """
        return self.delete(f"/api/posts/{post_id}/like")

    def get_post_likes(self, post_id: UUID) -> httpx.Response:
        """
        Получает информацию о лайках публикации.

        :param post_id: UUID публикации.
        :return: Ответ API со списком лайков или информацией о них.
        """
        return self.get(f"/api/posts/{post_id}/like")

    def post_like_comment(self, comment_id: UUID) -> httpx.Response:
        """
        Ставит лайк комментарию.

        :param comment_id: UUID комментария.
        :return: Ответ API с результатом добавления лайка.
        """
        return self.post(f"/api/comments/{comment_id}/like")

    def delete_unlike_comment(self, comment_id: UUID) -> httpx.Response:
        """
        Удаляет лайк с комментария.

        :param comment_id: UUID комментария.
        :return: Ответ API с результатом удаления лайка.
        """
        return self.delete(f"/api/comments/{comment_id}/like")