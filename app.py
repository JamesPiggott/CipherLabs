from flask import Flask
from flask_login import LoginManager

from config import Config

from core.users.processor.user_processor import UserProcessor

from core.users.database.user_database import UserDatabase
from settings.processor.app_settings_processor import AppSettingsProcessor

from blueprints.main.routes import main_blueprint
from blueprints.auth.routes import auth_blueprint
from blueprints.admin.routes import admin_blueprint
from blueprints.ciphers.routes import ciphers_blueprint


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return UserProcessor().retrieve_by_id(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.register_blueprint(ciphers_blueprint, url_prefix="/ciphers")

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)