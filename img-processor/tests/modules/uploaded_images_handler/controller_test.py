from conftest import client


def test_edit_user(client):
    response = client.post("/images", data={
        "name": "Flask",
        "theme": "dark",
    })
    assert response.status_code == 200
