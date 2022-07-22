from conftest import client

from app.utils.testing import upload_image, sample_images, get_sample_file_path
from app.modules.image.models import Image


def test_upload_image(client):
    image_file_name = sample_images[0]
    response = upload_image(client, image_file_name)
    image = Image.query.first()
    assert response.status_code == 201
    assert response.json["name"] == image.name
    assert response.json["uuid"] == image.uuid
    assert response.json["size"] == image.size
    assert response.json["width"] == image.width
    assert response.json["height"] == image.height
    assert response.json["storage_name"] == image.storage_name


def test_upload_image_returns_400_when_uploaded_file_is_not_a_valid_image(client):
    file_path = get_sample_file_path("sample.txt")
    with open(file_path, "rb") as f:
        response = client.post("image/upload", data={"image": (f, "sample.txt")})
        assert response.status_code == 400
        assert response.json["message"] == "Failed to upload image"


def test_upload_image_returns_400_when_no_file_was_uploaded(client):
    response = client.post("image/upload", data={})
    assert response.status_code == 400
    assert response.json["message"] == "Failed to upload image"
