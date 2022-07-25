import uuid

from fm_face.modules.target.models import Target
from fm_face.utils.testing.seeders import run_target_seeder


def test_get_all_targets(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/target' is requested (GET)
    THEN check that the response is valid
    """
    run_target_seeder()
    targets = Target.query.all()
    response = client.get("/target")

    assert response.status_code == 200
    assert len(response.json) == len(targets)

    for i, target in enumerate(targets):
        assert response.json[i]["uuid"] == target.uuid
        assert response.json[i]["title"] == target.title
        assert response.json[i]["description"] == target.description
        assert response.json[i]["results_uuid"] == target.results_uuid

        response_faces = response.json[i]["faces"]
        for j, face in enumerate(target.faces):
            assert response_faces[j]["uuid"] == face.uuid
            assert response_faces[j]["score"] == face.score
            assert response_faces[j]["image_uuid"] == face.image_uuid
            assert response_faces[j]["parent_uuid"] == face.parent_uuid

        response_tags = response.json[i]["tags"]
        for j, tag in enumerate(target.tags):
            assert response_tags[j]["name"] == tag.name


def test_get_all_targets_returns_nothing_if_db_is_empty(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/tagert' is requested (GET)
    THEN check that the response is valid and empty
    """
    response = client.get("/target")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_get_target_by_id(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/target/<target_id>' is requested (GET) with target_id that exist
    THEN check that the response is valid
    """
    run_target_seeder()
    target = Target.query.first()
    response = client.get(f"target/{target.uuid}")
    assert response.status_code == 200

    assert response.json["uuid"] == target.uuid
    assert response.json["title"] == target.title
    assert response.json["description"] == target.description
    assert response.json["results_uuid"] == target.results_uuid

    response_faces = response.json["faces"]
    for j, face in enumerate(target.faces):
        assert response_faces[j]["uuid"] == face.uuid
        assert response_faces[j]["score"] == face.score
        assert response_faces[j]["image_uuid"] == face.image_uuid
        assert response_faces[j]["parent_uuid"] == face.parent_uuid

    response_tags = response.json["tags"]
    for j, tag in enumerate(target.tags):
        assert response_tags[j]["name"] == tag.name


def test_get_target_by_id_returns_404_if_target_does_not_exist(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/target/<target_id>' is requested (GET) with target_id that does
         not exist
    THEN check that a '404' status code is returned
    """
    response = client.get(f"target/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "Target resource not found"
