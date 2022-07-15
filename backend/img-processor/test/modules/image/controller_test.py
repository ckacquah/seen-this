import uuid
import pytest

from conftest import client

from app.seeders import run_image_seeder, run_face_seeder
from app.modules.face.models import Face
from app.modules.image.models import Image
from app.modules.face.schemas import faces_schema, face_schema
from app.modules.image.schemas import images_schema, image_schema


def test_get_all_images_returns_images_stored_in_db(client):
    run_image_seeder()
    response = client.get("image/")
    assert response.status_code == 200
    assert len(response.json) == 5
    assert len(Image.query.all()) == 5
    assert images_schema.dump(Image.query.all()) == response.json


def test_get_all_images_returns_nothing_if_db_is_empty(client):
    response = client.get("image/")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_get_image_by_id(client):
    run_image_seeder()
    for image in Image.query.all():
        response = client.get(f"image/{image.uuid}")
        assert response.status_code == 200
        assert image_schema.dump(image) == response.json


def test_get_image_by_id_returns_404_if_image_does_not_exist(client):
    response = client.get(f"image/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "Image not found"


def test_delete_image_by_id(client):
    run_image_seeder()
    for index, image in enumerate(Image.query.all()):
        response = client.delete(f"image/{str(image.uuid)}")
        assert response.status_code == 200
        assert len(Image.query.all()) == 5 - index - 1
        assert response.json["message"] == "Image has been deleted successfully"


def test_delete_image_by_id_returns_404_if_image_does_not_exist(client):
    response = client.delete(f"image/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "Image not found"


def test_get_faces_extracted_by_image(client):
    run_face_seeder()
    for image in Image.query.all():
        response = client.get(f"image/{image.uuid}/faces")
        assert response.status_code == 200
        assert response.json == faces_schema.dump(
            Face.query.filter_by(parent_uuid=image.uuid)
        )


def test_get_faces_extracted_by_image_returns_404_if_image_does_not_exist(client):
    response = client.get(f"image/{str(uuid.uuid4())}/faces")
    assert response.status_code == 404
    assert response.json["message"] == "Image not found"
