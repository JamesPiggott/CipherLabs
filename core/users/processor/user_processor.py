from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

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

        existing_user = self.user_database.retrieve_by_username(username)

        if existing_user:
            raise ValueError("Username already exists.")

        existing_email = self.user_database.retrieve_by_email(email)

        if existing_email:
            raise ValueError("Email already exists.")

        password_hash = generate_password_hash(password)

        return self.user_database.create_user(
            username=username,
            email=email,
            password_hash=password_hash,
            is_admin=is_admin,
        )

    def authenticate_user(self, identifier, password):
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

    def retrieve_all_users(self):
        return self.user_database.retrieve_all()

    def count_admins(self):
        return self.user_database.count_admins()

    def update_user(self, user_id, username, email, is_admin, is_active, current_user_id=None):
        user = self.user_database.retrieve_by_id(user_id)

        if not user:
            raise ValueError("User not found.")

        username = username.strip()
        email = email.strip().lower()

        if not username:
            raise ValueError("Username is required.")

        if not email:
            raise ValueError("Email is required.")

        if str(user_id) == str(current_user_id):
            if not is_active:
                raise ValueError("You cannot deactivate your own account.")

            if user.is_admin and not is_admin and self.count_admins() <= 1:
                raise ValueError("You cannot remove the last admin account.")

        if user.is_admin and not is_admin and self.count_admins() <= 1:
            raise ValueError("At least one admin account must remain.")

        return self.user_database.update_user(
            user_id=user_id,
            username=username,
            email=email,
            is_admin=is_admin,
            is_active=is_active,
        )

    def update_password(self, user_id, password):
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")

        password_hash = generate_password_hash(password)

        return self.user_database.update_password(
            user_id=user_id,
            password_hash=password_hash,
        )

    def set_admin_status(self, user_id, is_admin):
        return self.user_database.set_admin_status(
            user_id=user_id,
            is_admin=is_admin,
        )

    def set_active_status(self, user_id, is_active):
        return self.user_database.set_active_status(
            user_id=user_id,
            is_active=is_active,
        )

    def delete_user(self, user_id, current_user_id=None):
        user = self.user_database.retrieve_by_id(user_id)

        if not user:
            raise ValueError("User not found.")

        if str(user_id) == str(current_user_id):
            raise ValueError("You cannot delete your own account.")

        if user.is_admin and self.count_admins() <= 1:
            raise ValueError("You cannot delete the last admin account.")

        return self.user_database.delete_user(user_id)

    def migrate_users_table(self):
        return self.user_database.migrate_table()

    def set_admin_by_username(self, username, is_admin=True):
        user = self.user_database.retrieve_by_username(username)

        if not user:
            raise ValueError("User not found.")

        return self.user_database.set_admin_by_username(
            username=username,
            is_admin=is_admin,
        )