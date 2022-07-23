from app.utils.testing import upload_image, sample_images, get_sample_file_path
from app.modules.image.models import Image


def test_upload_image(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/upload' is posted to (POST) with a valid image
    THEN check that the response is valid and that image is created
         successfully
    """
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


def test_upload_image_with_invalid_file(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/upload' is posted to (POST) with invalid an file
         not exist
    THEN check that a '400' status code is returned
    """
    file_path = get_sample_file_path("sample.txt")
    with open(file_path, "rb") as f:
        response = client.post(
            "image/upload", data={"image": (f, "sample.txt")}
        )
        assert response.status_code == 400
        assert response.json["message"] == "Failed to upload image"


def test_upload_image_without_any_file(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/upload' is posted to (POST) without an image
         not exist
    THEN check that a '400' status code is returned
    """
    response = client.post("image/upload", data={})
    assert response.status_code == 400
    assert response.json["message"] == "Failed to upload image"
