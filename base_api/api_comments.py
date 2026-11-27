import httpx
from uuid import UUID
from base_api.api import BaseAPI


class Comments(BaseAPI):
    """Клиент для работы с комментариями и ответами на комментарии."""

    def get_list_comments(self, post_id: UUID) -> httpx.Response:
        """
        Получает список комментариев к публикации.

        :param post_id: UUID публикации.
        :return: Ответ API со списком комментариев.
        """
        return self.get(f"/api/posts/{post_id}/comments")

    def post_create_comment(self, post_id: UUID, content: str) -> httpx.Response:
        """
        Создаёт комментарий к публикации.

        :param post_id: UUID публикации.
        :param content: Текст комментария.
        :return: Ответ API с созданным комментарием.
        """
        return self.post(
            f"/api/posts/{post_id}/comments",
            json={"content": content}
        )

    def patch_update_comment(self, comment_id: UUID, content: str) -> httpx.Response:
        """
        Обновляет текст комментария.

        :param comment_id: UUID комментария.
        :param content: Новый текст комментария.
        :return: Ответ API с обновлённым комментарием.
        """
        return self.patch(
            f"/api/comments/{comment_id}",
            json={"content": content}
        )

    def delete_comment(self, comment_id: UUID) -> httpx.Response:
        """
        Удаляет комментарий.

        :param comment_id: UUID комментария.
        :return: Ответ API о результате удаления.
        """
        return self.delete(f"/api/comments/{comment_id}")

    def get_list_replies(self, comment_id: UUID) -> httpx.Response:
        """
        Получает список ответов на комментарий.

        :param comment_id: UUID комментария.
        :return: Ответ API со списком ответов.
        """
        return self.get(f"/api/comments/{comment_id}/replies")

    def post_reply_comment(self, comment_id: UUID, content: str) -> httpx.Response:
        """
        Создаёт ответ на комментарий.

        :param comment_id: UUID комментария, на который создаётся ответ.
        :param content: Текст ответа.
        :return: Ответ API с созданным ответом.
        """
        return self.post(
            f"/api/comments/{comment_id}/replies",
            json={"content": content}
        )