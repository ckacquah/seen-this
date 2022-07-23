import uuid

from app.modules.image.models import Image
from app.seeders import run_image_seeder


def test_get_all_images(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image' is requested (GET)
    THEN check that the response is valid
    """
    run_image_seeder()
    images = Image.query.all()
    response = client.get("image/")
    assert response.status_code == 200
    assert len(response.json) == len(images)
    for i, image in enumerate(images):
        assert response.json[i]["uuid"] == image.uuid
        assert response.json[i]["name"] == image.name
        assert response.json[i]["size"] == image.size
        assert response.json[i]["width"] == image.width
        assert response.json[i]["height"] == image.height
        assert response.json[i]["storage_name"] == image.storage_name


def test_get_all_images_returns_nothing_if_db_is_empty(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image' is requested (GET)
    THEN check that the response is valid and empty
    """
    response = client.get("image/")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_get_image_by_id(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/<image_id>' is requested (GET) with image_id that exist
    THEN check that the response is valid
    """
    run_image_seeder()
    image = Image.query.first()
    response = client.get(f"image/{image.uuid}")
    assert response.status_code == 200
    assert response.json["uuid"] == image.uuid
    assert response.json["name"] == image.name
    assert response.json["size"] == image.size
    assert response.json["width"] == image.width
    assert response.json["height"] == image.height
    assert response.json["storage_name"] == image.storage_name


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
