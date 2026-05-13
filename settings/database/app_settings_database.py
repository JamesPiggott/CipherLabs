from core.database.database import db


class AppSettingsDatabase:

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """
        db.execute(query)

    def get_value(self, key):
        query = """
        SELECT value
        FROM app_settings
        WHERE key = %s;
        """
        row = db.fetch_one(query, (key,))

        if not row:
            return None

        return row["value"]

    def set_value(self, key, value):
        query = """
        INSERT INTO app_settings (key, value)
        VALUES (%s, %s)
        ON CONFLICT (key)
        DO UPDATE SET value = EXCLUDED.value;
        """
        db.execute(query, (key, value))