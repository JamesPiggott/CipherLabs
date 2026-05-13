from settings.database.app_settings_database import AppSettingsDatabase


class AppSettingsProcessor:

    REGISTRATION_ENABLED = "registration_enabled"

    def __init__(self):
        self.db = AppSettingsDatabase()

    def create_table(self):
        self.db.create_table()

    def is_registration_enabled(self):
        value = self.db.get_value(self.REGISTRATION_ENABLED)

        if value is None:
            return True

        return value.lower() == "true"

    def set_registration_enabled(self, enabled):
        self.db.set_value(
            self.REGISTRATION_ENABLED,
            "true" if enabled else "false",
        )