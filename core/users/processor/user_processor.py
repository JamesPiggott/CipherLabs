import uuid
from werkzeug.security import generate_password_hash, check_password_hash

from core.users.entities.user import User
from core.users.database.user_database import UserDatabase


class UserProcessor:
    def __init__(self):
        self.user_database = UserDatabase()

    def create_user(self, username, email, password, is_admin=False):
        username = username.strip()
        email = email.strip().lower()

        if not username:
            raise ValueError("Username is required.")

        if not email:
            raise ValueError("Email is required.")

        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")

        if self.user_database.retrieve_by_username(username):
            raise ValueError("Username is already in use.")

        if self.user_database.retrieve_by_email(email):
            raise ValueError("Email address is already in use.")

        user = User(
            user_id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=is_admin,
            is_active=True,
        )

        return self.user_database.create_user(user)

    def authenticate(self, identifier, password):
        identifier = identifier.strip()

        user = self.user_database.retrieve_by_username_or_email(identifier)

        if not user:
            return None

        if not user.is_active:
            return None

        if not check_password_hash(user.password_hash, password):
            return None

        return user

    def retrieve_by_id(self, user_id):
        return self.user_database.retrieve_by_id(user_id)