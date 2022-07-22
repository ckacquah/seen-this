import os
import cv2
import json
import pytest

from conftest import client
from app.modules.face.models import Face
from app.modules.image.models import Image
from app.utils import get_processed_face_path
from app.utils.testing import upload_image, get_sample_image_path
from app.tasks.extract_faces_from_image import (
    extract_faces_as_images,
    extract_faces_from_image,
    save_extracted_faces_to_db,
    save_extracted_faces_to_storage,
)


SAMPLE_FACES = [
    {
        "score": 0.9996384382247925,
        "facial_area": [353, 25, 387, 72],
    },
    {
        "score": 0.9996119141578674,
        "facial_area": [109, 65, 148, 112],
    },
    {
        "score": 0.9995879530906677,
        "facial_area": [456, 30, 495, 80],
    },
    {
        "score": 0.999541163444519,
        "facial_area": [261, 58, 297, 107],
    },
]


def test_extract_faces_from_image_task(client):
    upload_image(client, "sample.jpg")
    image = Image.query.first()
    results = extract_faces_from_image.apply(
        args=(
            {
                "image": image.uuid,
                "backend": "opencv",
            },
        ),
    ).get()
    assert results is not None
    assert results["faces"] is not None
    assert len(results["faces"]) == 5
    assert len(Image.query.all()) == 6
    assert len(Face.query.all()) == 5
    for face in Face.query.all():
        assert face.file is not None
        assert face.parent.uuid == image.uuid


def test_extract_faces_as_images(client):
    extract_faces = extract_faces_as_images(
        get_sample_image_path("sample.jpg"), SAMPLE_FACES
    )
    assert extract_faces is not None
    assert len(extract_faces) == 4
    for index, extract_face in enumerate(extract_faces):
        assert extract_face["score"] == SAMPLE_FACES[index]["score"]
        assert extract_face["facial_area"] == SAMPLE_FACES[index]["facial_area"]
        facial_area = SAMPLE_FACES[index]["facial_area"]
        image_height, image_width, image_channels = extract_face["image"].shape
        assert image_channels == 3
        assert image_width == facial_area[2] - facial_area[0]
        assert image_height == facial_area[3] - facial_area[1]


def test_save_extracted_faces_to_storage(client):
    extracted_faces = extract_faces_as_images(
        get_sample_image_path("sample.jpg"), SAMPLE_FACES
    )
    saved_faces = save_extracted_faces_to_storage(extracted_faces)
    for index, saved_face in enumerate(saved_faces):
        assert os.path.exists(get_processed_face_path(saved_face["file_name"]))
        assert saved_face["score"] == SAMPLE_FACES[index]["score"]
        assert saved_face["facial_area"] == SAMPLE_FACES[index]["facial_area"]
        img = cv2.imread(get_processed_face_path(saved_face["file_name"]))
        facial_area = SAMPLE_FACES[index]["facial_area"]
        image_height, image_width, image_channels = img.shape
        assert image_channels == 3
        assert image_width == facial_area[2] - facial_area[0]
        assert image_height == facial_area[3] - facial_area[1]


def test_save_extracted_faces_to_db(client):
    upload_image(client, "sample.jpg")
    image = Image.query.filter_by(name="sample.jpg").first()
    extracted_faces = extract_faces_as_images(
        get_sample_image_path("sample.jpg"), SAMPLE_FACES
    )
    saved_faces = save_extracted_faces_to_storage(extracted_faces)
    save_extracted_faces_to_db(saved_faces, parent=image)
    assert len(Image.query.all()) == 5
    assert len(Face.query.all()) == 4
    for face in Face.query.all():
        assert face.file is not None
        assert face.parent is not None
        assert Image.query.get(face.file.uuid) is not None
        assert Image.query.get(face.parent.uuid) is not None
        assert face.parent.uuid == image.uuid
