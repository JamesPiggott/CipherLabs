from app import create_app
from cipher.database.cipher_message_database import CipherMessageDatabase
from cipher.database.user_workspace_database import UserWorkspaceDatabase
from cipher.processor.user_workspace_processor import UserWorkspaceProcessor
from core.users.processor.user_processor import UserProcessor
from settings.processor.app_settings_processor import AppSettingsProcessor


def ensure_database_tables_exist():
    app = create_app()

    with app.app_context():
        UserProcessor().migrate_users_table()
        UserWorkspaceProcessor().migrate_user_workspaces_table()
        AppSettingsProcessor().create_table()
        CipherMessageDatabase().create_table()
        UserWorkspaceDatabase().create_table()

    print("Database tables checked successfully.")


if __name__ == "__main__":
    ensure_database_tables_exist()
