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

    def table_user(self, table_name, **filters):
        """Получает пользователя из БД по UUID."""
        query = f"select * from {table_name}"
        params = {}
        conditions = []
        for col, val in filters.items():
            conditions.append(f"{col} = :{col}")
            params[col] = val
        if conditions:
            query += " where " + " and ".join(conditions)
        with self.engine.connect() as conn:
            res = conn.execute(text(query), params)
            rows = res.fetchall()
        return len(rows)

    def count_posts(self, id):
        """Получение списка постов"""
        query = text("SELECT COUNT(*) FROM posts WHERE author_id = :id")
        params = {"id": id}
        with self.engine.connect() as conn:
            res = conn.execute(query, params)
            rows = res.scalar_one()
        return rows

    def count_followers(self, type_following, id):
        query = text(f"SELECT COUNT(*) FROM follows WHERE {type_following} = :id")
        params = {"id": id}
        with self.engine.connect() as conn:
            res = conn.execute(query, params)
            rows = res.scalar_one()
        return rows






