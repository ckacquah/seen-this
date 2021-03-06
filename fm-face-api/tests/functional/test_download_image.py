from api.utils import get_uploaded_file_path, get_processed_file_path
from api.utils.testing import upload_image, sample_images
from api.utils.testing.seeders import run_face_seeder
from api.modules.face.models import Face


def test_download_uploaded_image(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/download/<filename>' is requested (GET) with filename
         that exist
    THEN check that the response is valid and that the image has been
         downloaded successfully
    """
    response = upload_image(client, sample_images[0])
    storage_name = response.json["storage_name"]
    storage_path = get_uploaded_file_path(storage_name)
    response = client.get(f"image/download/{storage_name}")
    assert response.status_code == 200
    assert response.content_type == "image/jpeg"
    with open(storage_path, "rb") as img:
        assert response.data == img.read()


def test_download_processed_image(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/download/<filename>' is requested (GET) with filename
         that exist
    THEN check that the response is valid and that the image has been
         downloaded successfully
    """
    run_face_seeder()
    face = Face.query.first()
    storage_name = face.image.storage_name
    storage_path = get_processed_file_path(storage_name)
    response = client.get(f"image/download/{storage_name}")
    assert response.status_code == 200
    assert response.content_type == "image/jpeg"
    with open(storage_path, "rb") as img:
        assert response.data == img.read()


def test_download_image_with_unknown_filename(client):
    """
    GIVEN a flask application configured for testing
    WHEN the 'image/download/<filename>' is requested (GET) with filename that
         does not exist
    THEN check that a '404' status code is returned
    """
    response = client.get("image/download/01.jpg")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert response.json["message"] == "Image not found"
