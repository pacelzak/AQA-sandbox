import httpx
from base_api.api import BaseAPI


class Follows(BaseAPI):
    """Клиент для работы с подписками и запросами на подписку."""

    def post_follow_user(self, username: str) -> httpx.Response:
        """
        Отправляет запрос на подписку на пользователя.

        :param username: Имя пользователя, на которого нужно подписаться.
        :return: Ответ API с результатом отправки запроса на подписку.
        """
        return self.post(f"/api/users/{username}/follow")

    def delete_unfollow_user(self, username: str) -> httpx.Response:
        """
        Отписывается от пользователя.

        :param username: Имя пользователя, от которого нужно отписаться.
        :return: Ответ API с результатом отписки.
        """
        return self.delete(f"/api/users/{username}/follow")

    def get_follow_request(self) -> httpx.Response:
        """
        Получает список входящих запросов на подписку.

        :return: Ответ API со списком запросов на подписку.
        """
        return self.get("/api/follows/requests")

    def accept_follow_request(self, follow_id: str) -> httpx.Response:
        """
        Принимает входящий запрос на подписку.

        :param follow_id: UUID запроса на подписку.
        :return: Ответ API с результатом принятия запроса.
        """
        return self.post(f"/api/follows/requests/{follow_id}/accept")

    def reject_follow_request(self, follow_id: str) -> httpx.Response:
        """
        Отклоняет входящий запрос на подписку.

        :param follow_id: UUID запроса на подписку.
        :return: Ответ API с результатом отклонения запроса.
        """
        return self.post(f"/api/follows/requests/{follow_id}/reject")