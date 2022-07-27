import uuid
from unittest.mock import Mock

from api.modules.target.models import Target
from api.utils.testing.seeders import run_target_seeder


def test_get_all_targets(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/target' is requested (GET)
    THEN check that the response is valid
    """
    run_target_seeder()

    mock_targets_schema_dump = Mock(return_value=[])

    monkeypatch.setattr(
        "api.modules.target.controllers.targets_schema.dump",
        mock_targets_schema_dump,
    )

    targets = Target.query.all()
    response = client.get("/target")

    mock_targets_schema_dump.assert_called_once_with(targets)

    assert response.status_code == 200
    assert response.json == []


def test_get_all_targets_returns_nothing_if_db_is_empty(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/tagert' is requested (GET)
    THEN check that the response is valid and empty
    """
    response = client.get("/target")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_get_target_by_id(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/target/<target_id>' is requested (GET) with target_id that exist
    THEN check that the response is valid
    """
    run_target_seeder()

    mock_target_schema_dump = Mock(return_value={})

    monkeypatch.setattr(
        "api.modules.target.controllers.target_schema.dump",
        mock_target_schema_dump,
    )

    target = Target.query.first()
    response = client.get(f"target/{target.uuid}")

    mock_target_schema_dump.assert_called_once_with(target)

    assert response.status_code == 200
    assert response.json == {}


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
