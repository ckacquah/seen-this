from fm_face.config.testing import TestingConfig
from fm_face.config.production import ProductionConfig
from fm_face.config.development import DevelopmentConfig


def get_config(env):
    if env == "development":
        return DevelopmentConfig()
    elif env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
