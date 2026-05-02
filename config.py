import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB = os.getenv("POSTGRES_DB", "cipherlab")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "cipherlab_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")