import uuid

from api.utils.testing.seeders import run_target_seeder
from api.modules.target.models import Target


def test_delete_target_by_id(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/target/<target_id>' is deleted (DELETE) with invalid target_id
    THEN check that the response is valid and that target has been deleted
         successfully
    """
    run_target_seeder()
    target = Target.query.first()
    response = client.delete(f"target/{str(target.uuid)}")
    assert response.status_code == 200
    assert response.json["message"] == "target has been deleted successfully"
    assert target.query.get(target.uuid) is None
    assert len(target.query.all()) == 0


def test_delete_target_by_id_with_unknown_target_id(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/target/<target_id>' is deleted (DELETE) with target_id that does
         not exist
    THEN check that a '404' status code is returned and no changes happen to
         targets
    """
    response = client.delete(f"target/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "target not found"
