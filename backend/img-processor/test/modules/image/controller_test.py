import os
import pytest

from conftest import client

from app.seeders import run_image_seeder
from app.modules.image.models import Image
from app.modules.image.schemas import image_schema


def test_get_all_images_returns_images_stored_in_db(client):
    run_image_seeder()
    response = client.get("image/")
    assert response.status_code == 200
    assert len(response.json) == 5
    assert len(Image.query.all()) == 5
    for image_in_db, image_in_reponse in zip(Image.query.all(), response.json):
        assert image_in_db is not None
        assert image_in_reponse is not None
        assert image_schema.dump(image_in_db) == image_in_reponse


def test_get_all_images_returns_nothing_if_db_is_empty(client):
    response = client.get("image/")
    assert response.status_code == 200
    assert len(response.json) == 0
