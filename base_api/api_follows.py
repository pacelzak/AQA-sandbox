import httpx
from base_api.api import BaseAPI


class Follows(BaseAPI):

    """Клиент для управления подписками /api/auth (регистрация, вход, токены, профиль)."""

    def post_follow_user(self, username: str) -> httpx.Response:

        return self.post(f"/api/users/{username}/follow")

    def delete_unfollow_user(self, username: str) -> httpx.Response:

        return self.delete(f"/api/users/{username}/follow")

    def get_follow_request(self, username: str) -> httpx.Response:

        return self.get("/api/follows/requests")

    def accept_follow_request(self, follow_id: str) -> httpx.Response:

        return self.post(f"/api/follows/requests/{follow_id}/accept")


    def reject_follow_request(self, follow_id: str) -> httpx.Response:

        return self.post(f"/api/follows/requests/{follow_id}/reject")