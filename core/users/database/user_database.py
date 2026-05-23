import uuid

from core.database.database import db
from core.users.entities.user import User


class UserDatabase:

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
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
        self.migrate_users_to_uuid()

        query = """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS is_admin BOOLEAN NOT NULL DEFAULT FALSE;

        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE;
        """
        db.execute(query)

    def get_column_type(self, table_name, column_name):
        query = """
        SELECT data_type
        FROM information_schema.columns
        WHERE table_name = %s
        AND column_name = %s;
        """
        row = db.fetch_one(query, (table_name, column_name))

        if not row:
            return None

        return row["data_type"]

    def migrate_users_to_uuid(self):
        user_id_type = self.get_column_type("users", "id")

        if user_id_type == "uuid":
            return

        db.execute("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS id_uuid UUID;
        """)

        rows = db.fetch_all("""
        SELECT id, id_uuid
        FROM users;
        """)

        id_map = {}

        for row in rows:
            old_id = row["id"]
            new_id = row["id_uuid"] or str(uuid.uuid4())

            id_map[str(old_id)] = new_id

            db.execute(
                """
                UPDATE users
                SET id_uuid = %s
                WHERE id = %s;
                """,
                (new_id, old_id),
            )

        self.migrate_cipher_message_user_ids(id_map)
        self.migrate_workspace_user_ids(id_map)

        db.execute("""
        ALTER TABLE users
        ALTER COLUMN id_uuid SET NOT NULL;
        """)

        db.execute("""
        ALTER TABLE users
        DROP CONSTRAINT IF EXISTS users_pkey;
        """)

        db.execute("""
        ALTER TABLE users
        DROP COLUMN id;
        """)

        db.execute("""
        ALTER TABLE users
        RENAME COLUMN id_uuid TO id;
        """)

        db.execute("""
        ALTER TABLE users
        ADD PRIMARY KEY (id);
        """)

    def migrate_cipher_message_user_ids(self, id_map):
        column_type = self.get_column_type("cipher_messages", "created_by")

        if not column_type or column_type == "uuid":
            return

        db.execute("""
        ALTER TABLE cipher_messages
        ADD COLUMN IF NOT EXISTS created_by_uuid UUID;
        """)

        for old_id, new_id in id_map.items():
            db.execute(
                """
                UPDATE cipher_messages
                SET created_by_uuid = %s
                WHERE created_by = %s;
                """,
                (new_id, old_id),
            )

        db.execute("""
        ALTER TABLE cipher_messages
        DROP COLUMN created_by;
        """)

        db.execute("""
        ALTER TABLE cipher_messages
        RENAME COLUMN created_by_uuid TO created_by;
        """)

    def migrate_workspace_user_ids(self, id_map):
        column_type = self.get_column_type("user_workspaces", "user_id")

        if not column_type or column_type == "uuid":
            return

        db.execute("""
        ALTER TABLE user_workspaces
        DROP CONSTRAINT IF EXISTS user_workspaces_user_id_cipher_id_key;
        """)

        db.execute("""
        ALTER TABLE user_workspaces
        ADD COLUMN IF NOT EXISTS user_id_uuid UUID;
        """)

        for old_id, new_id in id_map.items():
            db.execute(
                """
                UPDATE user_workspaces
                SET user_id_uuid = %s
                WHERE user_id = %s;
                """,
                (new_id, old_id),
            )

        db.execute("""
        ALTER TABLE user_workspaces
        DROP COLUMN user_id;
        """)

        db.execute("""
        ALTER TABLE user_workspaces
        RENAME COLUMN user_id_uuid TO user_id;
        """)

        db.execute("""
        ALTER TABLE user_workspaces
        ALTER COLUMN user_id SET NOT NULL;
        """)

        db.execute("""
        ALTER TABLE user_workspaces
        ADD CONSTRAINT user_workspaces_user_id_cipher_id_key
        UNIQUE(user_id, cipher_id);
        """)

    def create_user(self, username, email, password_hash, is_admin=False):
        query = """
        INSERT INTO users (
            id,
            username,
            email,
            password_hash,
            is_admin
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
        """

        row = db.execute_returning(
            query,
            (str(uuid.uuid4()), username, email, password_hash, is_admin)
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

        row = db.execute_returning(query, (is_admin, user_id))

        return User.from_row(row)

    def set_active_status(self, user_id, is_active):
        query = """
        UPDATE users
        SET is_active = %s
        WHERE id = %s
        RETURNING *;
        """

        row = db.execute_returning(query, (is_active, user_id))

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

        row = db.execute_returning(query, (is_admin, username))

        return User.from_row(row)