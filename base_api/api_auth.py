from base_api.api import BaseAPI

class Auth(BaseAPI):

    def register(self, email, username, password, display_name):

        payload = {
          "email": email,
          "username": username,
          "password": password,
          "display_name": display_name
        }

        return self.post("/api/auth/register", json=payload)

    def login(self, email, password):

        payload = {
          "email": email,
          "password": password
        }
        return self.post("/api/auth/login", json=payload)

    def refresh(self, refresh_token):
        payload = {
          "refresh_token": refresh_token
        }
        return self.post("/api/auth/refresh", json=payload)

    def logout(self,refresh_token):

        payload = {"refresh_token": refresh_token}
        return self.post("/api/auth/logout", json=payload)

    def get_me(self):

        return self.get("/api/user/me")
