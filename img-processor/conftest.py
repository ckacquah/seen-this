import pytest
from app import app


@pytest.fixture()
def image_app():
    app.config.update({
        "TESTING": True,
    })
    yield image_app


@pytest.fixture()
def client(image_app):
    return app.test_client()


@pytest.fixture()
def runner(image_app):
    return app.test_cli_runner()
