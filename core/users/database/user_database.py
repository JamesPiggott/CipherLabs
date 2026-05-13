from core.database.database import db
from core.users.entities.user import User


class UserDatabase:

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT FALSE,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        db.execute(query)

    def migrate_table(self):
        query = """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS is_admin BOOLEAN NOT NULL DEFAULT FALSE;

        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE;
        """
        db.execute(query)

    def create_user(self, username, email, password_hash, is_admin=False):
        query = """
        INSERT INTO users (
            username,
            email,
            password_hash,
            is_admin
        )
        VALUES (%s, %s, %s, %s)
        RETURNING *;
        """

        row = db.execute_returning(
            query,
            (username, email, password_hash, is_admin)
        )

        return User.from_row(row)

    def retrieve_by_id(self, user_id):
        query = """
        SELECT *
        FROM users
        WHERE id = %s;
        """

        row = db.fetch_one(query, (user_id,))

        return User.from_row(row)

    def retrieve_by_email(self, email):
        query = """
        SELECT *
        FROM users
        WHERE email = %s;
        """

        row = db.fetch_one(query, (email,))

        return User.from_row(row)

    def retrieve_by_username(self, username):
        query = """
        SELECT *
        FROM users
        WHERE username = %s;
        """

        row = db.fetch_one(query, (username,))

        return User.from_row(row)

    def retrieve_by_username_or_email(self, identifier):
        query = """
        SELECT *
        FROM users
        WHERE username = %s OR email = %s;
        """

        row = db.fetch_one(query, (identifier, identifier))

        return User.from_row(row)


    def set_admin_status(self, user_id, is_admin):
        query = """
        UPDATE users
        SET is_admin = %s
        WHERE id = %s
        RETURNING *;
        """

        row = db.execute_returning(
            query,
            (is_admin, user_id)
        )

        return User.from_row(row)

    def set_active_status(self, user_id, is_active):
        query = """
        UPDATE users
        SET is_active = %s
        WHERE id = %s
        RETURNING *;
        """

        row = db.execute_returning(
            query,
            (is_active, user_id)
        )

        return User.from_row(row)


    def count_admins(self):
        query = """
        SELECT COUNT(*) AS admin_count
        FROM users
        WHERE is_admin = TRUE;
        """
        row = db.fetch_one(query)
        return row["admin_count"]

    def retrieve_all(self):
        query = """
        SELECT *
        FROM users
        ORDER BY created_at DESC;
        """
        rows = db.fetch_all(query)
        return [User.from_row(row) for row in rows]

    def update_user(self, user_id, username, email, is_admin, is_active):
        query = """
        UPDATE users
        SET username = %s,
            email = %s,
            is_admin = %s,
            is_active = %s
        WHERE id = %s
        RETURNING *;
        """
        row = db.execute_returning(
            query,
            (username, email, is_admin, is_active, user_id),
        )
        return User.from_row(row)

    def update_password(self, user_id, password_hash):
        query = """
        UPDATE users
        SET password_hash = %s
        WHERE id = %s
        RETURNING *;
        """
        row = db.execute_returning(query, (password_hash, user_id))
        return User.from_row(row)

    def delete_user(self, user_id):
        query = """
        DELETE FROM users
        WHERE id = %s;
        """
        db.execute(query, (user_id,))

    def set_admin_by_username(self, username, is_admin=True):
        query = """
        UPDATE users
        SET is_admin = %s
        WHERE username = %s
        RETURNING *;
        """

        row = db.execute_returning(
            query,
            (is_admin, username)
        )

        return User.from_row(row)