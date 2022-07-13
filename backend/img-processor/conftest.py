import pytest
import logging

from app import create_app, db
from app.utils.testing import (
    config,
    delete_uploaded_files,
    delete_processed_files,
)


@pytest.fixture()
def app():
    app = create_app(config=config)
    # setup test app context
    with app.app_context():
        # setup test database
        db.create_all()
        yield app
        # teardown test database
        db.session.remove()
        db.drop_all()

    delete_uploaded_files()
    delete_processed_files()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
