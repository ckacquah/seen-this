import os
import pytest
import logging
import tempfile

from app import app, db
from config import SAMPLES_FOLDER, PROCESSED_FACES_FOLDER

# Remove faker logs during tests
logger = logging.getLogger("faker")
logger.setLevel(logging.INFO)

sample_images = ["01.jpeg", "02.jpeg", "03.jpeg", "04.jpeg", "05.jpeg"]


def delete_all_processed_faces_on_disk():
    filelist = os.listdir(PROCESSED_FACES_FOLDER)
    for f in filelist:
        os.remove(os.path.join(PROCESSED_FACES_FOLDER, f))


def get_sample_image_path(filename):
    return os.path.join(SAMPLES_FOLDER, "images", filename)


def get_sample_file_path(filename):
    return os.path.join(SAMPLES_FOLDER, "files", filename)


def upload_image(client, image_name):
    image_path = get_sample_image_path(image_name)
    with open(image_path, "rb") as img:
        response = client.post("images/upload", data={"image": (img, image_name)})
    return response


def upload_images(client, images=sample_images):
    for image in images:
        upload_image(client, image)


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
    delete_all_processed_faces_on_disk()

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