import uuid

from fm_face.utils.testing.seeders import run_face_seeder
from fm_face.modules.face.models import Face


def test_delete_face_by_id(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/face/<face_id>' is deleted (DELETE) with face_id that exist
    THEN check that the response is valid and the face has deleted successfully
    """
    run_face_seeder()
    for i, face in enumerate(Face.query.all()):
        response = client.delete(f"face/{str(face.uuid)}")
        assert response.status_code == 200
        assert response.json["message"] == "Face has been deleted successfully"
        assert Face.query.get(face.uuid) is None
        assert len(Face.query.all()) == 4 - i


def test_delete_face_by_id_with_unknown_face_id(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/face/<face_id>' is deleted (DELETE) with face_id that does
         not exist
    THEN check that a '404' status code is returned and that no changes happen
         to the faces
    """
    before = Face.query.all()
    response = client.delete(f"face/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "Face not found"
    assert before == Face.query.all()
