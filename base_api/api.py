import httpx
from helpers.settings import Settings


class BaseAPI:

    def __init__(self, client=None):

        self.client = client or httpx.Client(base_url=Settings.BASE_URL)

    def requests(self, method, path, **kwargs):

        return self.client.request(method, path, **kwargs,)

    def set_token(self, token):

        self.client.headers.update({"Authorization": f"Bearer {token}"})

    def get(self,path, **kwargs):

        return self.requests("GET", path, **kwargs)

    def post(self,path, **kwargs):

        return self.requests("POST", path, **kwargs)

    def put(self,path, **kwargs):

        return self.requests("PUT", path, **kwargs)

    def patch(self,path, **kwargs):

        return self.requests("PATCH", path, **kwargs)

    def delete(self,path, **kwargs):

        return self.requests("DELETE", path, **kwargs)



