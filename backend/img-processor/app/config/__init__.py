from app.config.testing import TestingConfig
from app.config.production import ProductionConfig
from app.config.development import DevelopmentConfig


def get_config(env):
    if env == "development":
        return DevelopmentConfig()
    elif env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return Config()
