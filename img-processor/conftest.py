import os
import pytest
import logging

from app import app

# Remove faker logs during tests
logger = logging.getLogger('faker')
logger.setLevel(logging.INFO)


samples_folder = os.path.join(app.root_path, '../samples')


def get_sample_image_path(filename):
    return os.path.join(samples_folder, 'images', filename)


@pytest.fixture(scope="module")
def image_app():
    app.config.update({
        "TESTING": True,
    })
    ctx = app.app_context()
    ctx.push()
    yield image_app
    ctx.pop()


@pytest.fixture()
def client(image_app):
    return app.test_client()


@pytest.fixture()
def runner(image_app):
    return app.test_cli_runner()
