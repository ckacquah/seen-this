import os
import pytest

from conftest import db, client

from app.tasks import celery
from app.modules.image.models import File, Face
from app.utils.testing import (
    upload_image,
    upload_images,
    sample_images,
    get_sample_file_path,
)


def test_images_can_be_uploaded(client):
    for image in sample_images:
        response = upload_image(client, image)
        assert response.status_code == 200
        assert response.json["message"] == "Image uploaded successfully"
        assert response.json["image_name"] == image
        assert File.query.get(response.json["uuid"]) is not None


def test_only_images_can_be_uploaded(client):
    file = get_sample_file_path("sample.txt")
    with open(file, "rb") as f:
        response = client.post("images/upload", data={"image": (f, "sample.txt")})
    assert response.status_code == 400
    assert response.json["message"] == "Only images can be uploaded"


def test_image_cannot_be_empty(client):
    response = client.post("images/upload", data={"image": (None, "")})
    assert response.status_code == 400
    assert response.json["message"] == "Image cannot be empty"


def test_image_part_cannot_be_empty(client):
    response = client.post("images/upload", data={})
    assert response.status_code == 400
    assert response.json["message"] == "No image file part"


def test_images_can_be_retrieved(client):
    upload_images(client)
    response = client.get("images/")
    assert response.status_code == 200
    assert response.json["message"] == "Images retrieved successfully"
    assert len(response.json["images"]) == 5
    for image in response.json["images"]:
        assert image["name"] in sample_images
        assert File.query.get(image["uuid"]) is not None


@pytest.fixture()
def test_faces_can_be_extracted_from_image(client):
    upload_image(client, "sample.jpg")
    file = File.query.filter_by(name="sample.jpg").first()
    assert file is not None
    response = client.post(
        "images/extract-faces",
        data={
            "image": file.uuid,
            "backend": "retinaface",
        },
    )
    assert response.status_code == 200
    assert response.json["message"] == "Face extraction started successful"
    assert response.json["task_id"] is not None
    task_result = celery.AsyncResult(response.json["task_id"])
    assert task_result.status == "SUCCESS" or task_result.status == "STARTED"
