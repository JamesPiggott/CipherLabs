import psycopg2
import psycopg2.extras
from flask import current_app


class DBConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection is None or self.connection.closed:
            self.connection = psycopg2.connect(
                host=current_app.config["POSTGRES_HOST"],
                port=current_app.config["POSTGRES_PORT"],
                dbname=current_app.config["POSTGRES_DB"],
                user=current_app.config["POSTGRES_USER"],
                password=current_app.config["POSTGRES_PASSWORD"],
            )

        return self.connection

    def fetch_one(self, query, params=None):
        conn = self.connect()

        try:
            with conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            ) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchone()

        except Exception:
            conn.rollback()
            raise

    def fetch_all(self, query, params=None):
        conn = self.connect()

        try:
            with conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            ) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()

        except Exception:
            conn.rollback()
            raise

    def execute(self, query, params=None):
        conn = self.connect()

        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())

            conn.commit()

        except Exception:
            conn.rollback()
            raise

    def execute_returning(self, query, params=None):
        conn = self.connect()

        try:
            with conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            ) as cursor:
                cursor.execute(query, params or ())
                result = cursor.fetchone()

            conn.commit()

            return result

        except Exception:
            conn.rollback()
            raise