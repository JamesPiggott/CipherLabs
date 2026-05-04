class UserWorkspace:
    def __init__(
        self,
        workspace_id,
        user_id,
        cipher_id,
        substitution_mapping=None,
        notes=None,
        created_at=None,
        updated_at=None,
    ):
        self.id = workspace_id
        self.user_id = user_id
        self.cipher_id = cipher_id
        self.substitution_mapping = substitution_mapping or {}
        self.notes = notes or ""
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def from_row(row):
        if not row:
            return None

        return UserWorkspace(
            workspace_id=row["id"],
            user_id=row["user_id"],
            cipher_id=row["cipher_id"],
            substitution_mapping=row.get("substitution_mapping") or {},
            notes=row.get("notes"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )