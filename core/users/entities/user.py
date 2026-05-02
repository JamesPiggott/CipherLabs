from flask_login import UserMixin


class User(UserMixin):
    def __init__(
        self,
        user_id,
        username,
        email,
        password_hash=None,
        is_admin=False,
        is_active=True,
        created_at=None,
    ):
        self.id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self._is_active = is_active
        self.created_at = created_at

    @property
    def is_active(self):
        return self._is_active

    @staticmethod
    def from_row(row):
        if not row:
            return None

        return User(
            user_id=row["id"],
            username=row["username"],
            email=row["email"],
            password_hash=row.get("password_hash"),
            is_admin=row.get("is_admin", False),
            is_active=row.get("is_active", True),
            created_at=row.get("created_at"),
        )