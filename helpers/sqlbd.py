from sqlalchemy import create_engine, text
from helpers.settings import Settings


class SQLBD:

    def __init__(self):
        self.engine = create_engine(Settings.CONNECTION_BD)

    def info_user(self, uuid):
        """Получает пользователя из БД по UUID."""
        query = text("SELECT * FROM users WHERE id = :id")
        params = {"id": uuid}

        with self.engine.connect() as connection:
            result = connection.execute(query, params)
            return result.fetchone()



