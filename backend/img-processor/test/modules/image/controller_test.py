import uuid
import pytest

from conftest import client

from app.seeders import run_image_seeder, run_face_seeder
from app.utils import get_uploaded_file_path
from app.utils.testing import upload_image, sample_images, get_sample_file_path
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
        assert Image.query.get(image.uuid) is None
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


def test_upload_image(client):
    image = sample_images[0]
    response = upload_image(client, image)
    assert response.status_code == 201
    assert response.json["name"] == image
    assert image_schema.dump(Image.query.get(response.json["uuid"])) == response.json


def test_upload_image_returns_400_when_uploaded_file_is_not_a_valid_image(client):
    sample_text_file = get_sample_file_path("sample.txt")
    with open(sample_text_file, "rb") as f:
        response = client.post("image/upload", data={"image": (f, "sample.txt")})
    assert response.status_code == 400
    assert response.json["message"] == "Failed to upload image"


def test_upload_image_returns_400_when_no_file_was_uploaded(client):
    response = client.post("image/upload", data={})
    assert response.status_code == 400
    assert response.json["message"] == "Failed to upload image"


def test_download_uploaded_image(client):
    uploaded_image = upload_image(client, sample_images[0]).json
    response = client.get(f"image/download/{uploaded_image['storage_name']}")
    assert response.status_code == 200
    assert response.content_type == "image/jpeg"
    image = Image.query.filter_by(storage_name=uploaded_image["storage_name"]).first()
    assert image is not None
    with open(get_uploaded_file_path(image.storage_name), "rb") as img:
        img_content = img.read()
    assert response.data == img_content


def test_download_uploaded_image_returns_404_when_file_is_not_found(client):
    response = client.get(f"image/download/01.jpg")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert response.json["message"] == "Image not found"
