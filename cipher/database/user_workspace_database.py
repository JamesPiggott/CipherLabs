import json

from cipher.entities.user_workspace import UserWorkspace
from core.database.database import db


class UserWorkspaceDatabase:
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS user_workspaces (
            id UUID PRIMARY KEY,
            user_id INTEGER NOT NULL,
            cipher_id UUID NOT NULL,
            substitution_mapping JSONB NOT NULL DEFAULT '{}',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, cipher_id)
        );
        """
        db.execute(query)

    def migrate_table(self):
        query = """
        ALTER TABLE user_workspaces
        ALTER COLUMN user_id TYPE INTEGER
        USING user_id::text::integer;
        """
        db.execute(query)

    def retrieve_by_user_and_cipher(self, user_id, cipher_id):
        query = """
        SELECT *
        FROM user_workspaces
        WHERE user_id = %s AND cipher_id = %s;
        """

        row = db.fetch_one(query, (user_id, cipher_id))

        return UserWorkspace.from_row(row)

    def upsert_workspace(self, workspace):
        query = """
        INSERT INTO user_workspaces (
            id,
            user_id,
            cipher_id,
            substitution_mapping,
            notes
        )
        VALUES (%s, %s, %s, %s, %s)

        ON CONFLICT (user_id, cipher_id)
        DO UPDATE SET
            substitution_mapping = EXCLUDED.substitution_mapping,
            notes = EXCLUDED.notes,
            updated_at = CURRENT_TIMESTAMP

        RETURNING *;
        """

        row = db.execute_returning(
            query,
            (
                workspace.id,
                workspace.user_id,
                workspace.cipher_id,
                json.dumps(workspace.substitution_mapping),
                workspace.notes,
            ),
        )

        return UserWorkspace.from_row(row)