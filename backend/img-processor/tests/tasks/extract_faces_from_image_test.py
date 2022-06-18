import pytest

from app.modules.image_handler.models import File
from app.tasks.extract_faces_from_image import extract_faces_from_image

from conftest import client, upload_image


def test_extract_faces_from_image_task(client):
    upload_image(client, "sample.jpg")
    file = File.query.filter_by(name="sample.jpg").first()
    assert extract_faces_from_image.apply(args=({},)) is not None
    results = extract_faces_from_image.apply(
        args=(
            {
                "image": file.uuid,
                "backend": "opencv",
            },
        ),
    ).get()
    assert results is not None
    assert results["faces"] is not None
    assert len(results["faces"]) == 5


def test_save_extracted_faces_to_processed_folder(client):
    upload_image(client, "sample.jpg")
    pass
