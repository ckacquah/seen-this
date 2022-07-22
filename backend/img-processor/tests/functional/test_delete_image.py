import uuid

from conftest import client

from app.seeders import run_image_seeder
from app.modules.image.models import Image


def test_delete_image_by_id(client):
    run_image_seeder()
    for i, image in enumerate(Image.query.all()):
        response = client.delete(f"image/{str(image.uuid)}")
        assert response.status_code == 200
        assert response.json["message"] == "Image has been deleted successfully"
        assert Image.query.get(image.uuid) is None
        assert len(Image.query.all()) == 4 - i


def test_delete_image_by_id_returns_404_if_image_does_not_exist(client):
    response = client.delete(f"image/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "Image not found"
