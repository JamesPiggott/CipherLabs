from app import create_app
from core.users.database.user_database import UserDatabase


def ensure_database_tables_exist():
    app = create_app()

    with app.app_context():
        UserDatabase().create_table()

    print("Database tables checked successfully.")


if __name__ == "__main__":
    ensure_database_tables_exist()