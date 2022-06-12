import os

from conftest import client, get_sample_image_path


def test_images_can_be_uploaded(client):
    images = ["01.jpeg", "02.jpeg", "03.jpeg", "04.jpeg", "05.jpeg"]
    for image in images:
        with open(get_sample_image_path(image), "rb") as img:
            response = client.post("images/upload", data={
                "image": (img, image)
            })

        assert response.status_code == 200
        assert response.json['message'] == 'Image uploaded successfully'
        assert response.json['image_name'] == image
