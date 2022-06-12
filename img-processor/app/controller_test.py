import os
from conftest import client, get_sample_image_path


def test_user_can_upload_image(client):
    data = {
        "image": (
            open(get_sample_image_path('01.jpeg'), 'rb'),
            '01.jpeg'
        )
    }
    response = client.post("images/upload", data=data)
    assert response.status_code == 200
    assert response.json['message'] == 'Image uploaded successfully'
    assert response.json['image_name'] == '01.jpeg'
