import os

from api.config.base import Config


class DevelopmentConfig(Config):
    DEBUG = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return "sqlite:///" + os.path.join(
            self.DATABASE_FOLDER, "development.db"
        )
