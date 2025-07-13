from backend.app.core.config import settings
import psycopg2

class ConnectDataBase:
    def __init__(self):
        self.host = settings.POSTGRES_HOST
        self.port = settings.POSTGRES_PORT
        self.username = settings.POSTGRES_USER
        self.password = settings.POSTGRES_PASSWORD
        self.database = settings.POSTGRES_DB
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            host = self.host,
            port = self.port,
            database = self.database,
            user = self.username,
            password = self.password
        )
        return self.connection

    def insert_one_query(self, sql, val):
        try:
            cur = self.connection.cursor()
            cur.execute(sql, val)
            self.connection.commit()
            cur.close()

        except Exception as e:
            print(f"Insert One Error: {e}")
            self.connection.rollback()

    def insert_many_query(self, sql, val):
        try:
            cur = self.connection.cursor()
            cur.executemany(sql, val)
            self.connection.commit()
            cur.close()

        except Exception as e:
            print(f"Insert Many Error: {e}")
            self.connection.rollback()

    def select_one_query(self, sql, val):
        try:
            cur = self.connection.cursor()
            cur.execute(sql, val)
            record = cur.fetchone()
            return record

        except Exception as e:
            print(f"Select One Error {e}")
            return None

    def select_many_query(self, sql, val):
        try:
            cur = self.connection.cursor()
            cur.execute(sql, val)
            record = cur.fetchall()
            return record

        except Exception as e:
            print(f"Select Many Error {e}")
            return None
