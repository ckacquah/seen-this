import uuid

from api.utils.testing.seeders import run_image_seeder
from api.modules.image.models import Image


def test_delete_image_by_id(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/<image_id>' is deleted (DELETE) with image_id that exist
    THEN check that the response is valid and that image has been deleted
         successfully
    """
    run_image_seeder()
    for i, image in enumerate(Image.query.all()):
        response = client.delete(f"image/{str(image.uuid)}")
        assert response.status_code == 200
        assert (
            response.json["message"] == "Image has been deleted successfully"
        )
        assert Image.query.get(image.uuid) is None
        assert len(Image.query.all()) == 4 - i


def test_delete_image_by_id_with_unknown_image_id(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/<image_id>' is deleted (DELETE) with image_id that does
         not exist
    THEN check that a '404' status code is returned and no changes happen to
         images
    """
    response = client.delete(f"image/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "Image not found"
