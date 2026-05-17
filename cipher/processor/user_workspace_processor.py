import uuid

from cipher.entities.user_workspace import UserWorkspace
from cipher.database.user_workspace_database import UserWorkspaceDatabase


class UserWorkspaceProcessor:
    def __init__(self):
        self.database = UserWorkspaceDatabase()

    def get_workspace(self, user_id, cipher_id):
        return self.database.retrieve_by_user_and_cipher(user_id, cipher_id)

    def save_workspace(self, user_id, cipher_id, substitution_mapping, notes=""):
        workspace = UserWorkspace(
            workspace_id=str(uuid.uuid4()),
            user_id=user_id,
            cipher_id=cipher_id,
            substitution_mapping=substitution_mapping or {},
            notes=notes or "",
        )

        return self.database.upsert_workspace(workspace)

    def migrate_user_workspaces_table(self):
        return self.database.migrate_table()
