from app.config.base import Config


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
