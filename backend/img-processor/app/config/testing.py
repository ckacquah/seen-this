import os
from app.config.base import Config


class TestingConfig(Config):
    DEBUG = True
    TESTING = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return "sqlite:///" + os.path.join(self.DATABASE_FOLDER, "testing.db")
