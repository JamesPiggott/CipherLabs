from app import create_app
from core.users.processor.user_processor import UserProcessor


def main():
    username = "JamesPiggott"

    app = create_app()

    with app.app_context():
        user = UserProcessor().set_admin_by_username(
            username=username,
            is_admin=True,
        )

        print(f"User '{user.username}' is now admin.")


if __name__ == "__main__":
    main()