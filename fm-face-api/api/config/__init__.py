from api.config.testing import TestingConfig
from api.config.production import ProductionConfig
from api.config.development import DevelopmentConfig


def get_config(env):
    if env == "development":
        return DevelopmentConfig()
    elif env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
