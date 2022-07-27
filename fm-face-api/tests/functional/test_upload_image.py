from unittest.mock import Mock
from api.utils.testing import (
    upload_image,
    sample_images,
    get_sample_file_path,
)
from api.modules.image.models import Image


def test_upload_image(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/upload' is posted to (POST) with a valid image
    THEN check that the response is valid and that image is created
         successfully
    """
    image_file_name = sample_images[0]

    mock_image_schema_dump = Mock(return_value={})

    monkeypatch.setattr(
        "api.modules.image.controllers.image_schema.dump",
        mock_image_schema_dump,
    )

    response = upload_image(client, image_file_name)
    image = Image.query.first()

    mock_image_schema_dump.assert_called_once_with(image)

    assert response.status_code == 201
    assert response.json == {}


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
    THEN check that a '400' status code is returned
    """
    response = client.post("image/upload", data={})
    assert response.status_code == 400
    assert response.json["message"] == "Failed to upload image"
