import uuid
from unittest.mock import Mock

from api.modules.image.models import Image
from api.utils.testing.seeders import run_image_seeder


def test_get_all_images(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image' is requested (GET)
    THEN check that the response is valid
    """
    run_image_seeder()

    mock_images_schema_dump = Mock(return_value=[])

    monkeypatch.setattr(
        "api.modules.image.controllers.images_schema.dump",
        mock_images_schema_dump,
    )

    images = Image.query.all()
    response = client.get("image/")

    mock_images_schema_dump.assert_called_once_with(images)

    assert response.status_code == 200
    assert response.json == []


def test_get_all_images_returns_nothing_if_db_is_empty(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image' is requested (GET)
    THEN check that the response is valid and empty
    """
    response = client.get("image/")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_get_image_by_id(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/<image_id>' is requested (GET) with image_id that exist
    THEN check that the response is valid
    """
    run_image_seeder()

    mock_image_schema_dump = Mock(return_value={})

    monkeypatch.setattr(
        "api.modules.image.controllers.image_schema.dump",
        mock_image_schema_dump,
    )

    image = Image.query.first()
    response = client.get(f"image/{image.uuid}")

    mock_image_schema_dump.assert_called_once_with(image)

    assert response.status_code == 200
    assert response.json == {}


def test_get_image_by_id_returns_404_if_image_does_not_exist(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/<image_id>' is requested (GET) with image_id that does
         not exist
    THEN check that a '404' status code is returned
    """
    response = client.get(f"image/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "Image not found"
