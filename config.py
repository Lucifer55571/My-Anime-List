import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Konfigurasi utama aplikasi Flask
    """

    SECRET_KEY = os.environ.get("SECRET_KEY", "my-anime-list-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "images")
    ANIME_PER_PAGE = 8
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"