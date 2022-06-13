import os

from conftest import db, client, get_sample_image_path, get_sample_file_path
from app.modules.image_handler.models import File

sample_images = ["01.jpeg", "02.jpeg", "03.jpeg", "04.jpeg", "05.jpeg"]


def upload_image(client, image_name):
    image_path = get_sample_image_path(image_name)
    with open(image_path, "rb") as img:
        response = client.post("images/upload", data={"image": (img, image_name)})
    return response


def upload_images(client, images=sample_images):
    for image in images:
        upload_image(client, image)


def test_images_can_be_uploaded(client):
    for image in sample_images:
        response = upload_image(client, image)
        assert response.status_code == 200
        assert response.json["message"] == "Image uploaded successfully"
        assert response.json["image_name"] == image
        assert (
            File.query.filter_by(name=image, uuid=response.json["uuid"]).first()
            is not None
        )


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
        assert (
            File.query.filter_by(name=image["name"], uuid=image["uuid"]).first()
            is not None
        )
