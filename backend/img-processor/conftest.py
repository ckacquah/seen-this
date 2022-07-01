import pytest
import logging

from app import create_app, db
from app.config.testing import TestingConfig
from app.utils.testing import delete_all_processed_faces_on_disk

# Remove faker logs during tests
logger = logging.getLogger("faker")
logger.setLevel(logging.INFO)


@pytest.fixture()
def app():
    app = create_app(config=TestingConfig())
    # setup test app context
    with app.app_context():
        # setup test database
        db.create_all()
        yield app
        # teardown test database
        db.session.remove()
        db.drop_all()

    delete_all_processed_faces_on_disk()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
