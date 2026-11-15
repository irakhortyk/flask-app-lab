import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if not os.path.exists(os.path.join(BASE_DIR, "run.py")):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY", "flask-lab6-secret-key")
DEBUG = True
MAX_CONTENT_LENGTH = 5 * 1024 * 1024


class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'data.sqlite')}"
    )


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'data.sqlite')}"
    )


config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}