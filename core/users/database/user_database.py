from core.database.database import db
from core.users.entities.user import User


class UserDatabase:
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            username VARCHAR(80) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT FALSE,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        db.execute(query)

    def create_user(self, user):
        query = """
        INSERT INTO users (
            id, username, email, password_hash, is_admin, is_active
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *;
        """
        row = db.execute_returning(
            query,
            (
                user.id,
                user.username,
                user.email,
                user.password_hash,
                user.is_admin,
                user.is_active,
            ),
        )
        return User.from_row(row)

    def retrieve_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = %s;"
        row = db.fetch_one(query, (user_id,))
        return User.from_row(row)

    def retrieve_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s;"
        row = db.fetch_one(query, (username,))
        return User.from_row(row)

    def retrieve_by_email(self, email):
        query = "SELECT * FROM users WHERE email = %s;"
        row = db.fetch_one(query, (email,))
        return User.from_row(row)

    def retrieve_by_username_or_email(self, identifier):
        query = """
        SELECT *
        FROM users
        WHERE username = %s OR email = %s;
        """
        row = db.fetch_one(query, (identifier, identifier))
        return User.from_row(row)