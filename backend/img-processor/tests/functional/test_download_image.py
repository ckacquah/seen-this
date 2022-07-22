from conftest import client

from app.utils import get_uploaded_file_path
from app.utils.testing import upload_image, sample_images


def test_download_uploaded_image(client):
    response = upload_image(client, sample_images[0])
    storage_name = response.json["storage_name"]
    storage_path = get_uploaded_file_path(storage_name)
    response = client.get(f"image/download/{storage_name}")
    assert response.status_code == 200
    assert response.content_type == "image/jpeg"
    with open(storage_path, "rb") as img:
        assert response.data == img.read()


def test_download_uploaded_image_returns_404_when_file_is_not_found(client):
    response = client.get(f"image/download/01.jpg")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert response.json["message"] == "Image not found"
