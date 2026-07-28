import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def get_database_uri():
    """
    Prioritas:
    1. DATABASE_URL dari environment variable (untuk deployment)
    2. MySQL Files.io (default)
    """

    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return database_url

    return (
        "mysql+mysqlconnector://"
        "db_anime_funnysheep:"
        "73f3d6dfd1ff785ce8fb8fac1c54507b192832c5"
        "@etb5k4.h.filess.io:3306/"
        "db_anime_funnysheep"
    )

class Config:
    """
    Konfigurasi utama aplikasi Flask
    """
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "my-anime-list-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "images")

    ANIME_PER_PAGE = 8

    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"