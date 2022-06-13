import os
import pytest
import logging
import tempfile

from app import app, db

# Remove faker logs during tests
logger = logging.getLogger("faker")
logger.setLevel(logging.INFO)


samples_folder = os.path.join(app.root_path, "../samples")


def get_sample_image_path(filename):
    return os.path.join(samples_folder, "images", filename)

def get_sample_file_path(filename):
    return os.path.join(samples_folder, "files", filename)

@pytest.fixture
def image_app():
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    # setup test app context
    ctx = app.app_context()
    ctx.push()
    # setup test database
    db.create_all()

    yield image_app
    
    # teardown test database
    db.drop_all()
    db.session.remove()
    # remove test app context
    ctx.pop()


@pytest.fixture()
def client(image_app):
    return app.test_client()


@pytest.fixture()
def runner(image_app):
    return app.test_cli_runner()
