import PIL
from unittest.mock import Mock, call

from fm_face.jobs.extract_faces_from_image import extract_faces_from_image
from fm_face.utils.testing.seeders import run_image_seeder
from fm_face.modules.face.models import Face
from fm_face.modules.image.models import Image
from fm_face.modules.image.services import (
    detect_faces_from_image,
    store_detected_faces_to_db,
    store_processed_image_info_to_db,
    store_detected_faces_image_info_to_db,
    store_PIL_Image_as_jpeg_in_processed_folder,
    store_detected_faces_images_to_processed_folder,
)
from fm_face.utils.testing import (
    get_sample_image_path,
    no_image_pixel_differences,
)

SAMPLE_IMAGE_PATH = get_sample_image_path("sample.jpg")

SAMPLE_PIL_IMAGE = PIL.Image.open(SAMPLE_IMAGE_PATH)

PROCESSED_IMAGE_INFO = {
    "size": 666,
    "width": 666,
    "height": 666,
    "file_name": "image.jpg",
}

SAMPLE_FACES = {
    "face_1": {
        "score": 0.9995879530906677,
        "facial_area": [456, 30, 495, 80],
    },
    "face_2": {
        "score": 0.9995411634445019,
        "facial_area": [261, 58, 297, 107],
    },
}


def test_extract_faces_from_image_object(client, monkeypatch):
    """
    GIVEN an Image object
    WHEN faces are extracted from the image
    THEN check that faces are extracted and stored correctly
    """
    run_image_seeder()
    image = Image.query.first()

    mock_get_uploaded_file_path = Mock(return_value=SAMPLE_IMAGE_PATH)
    mock_detect_faces_from_image = Mock(return_value=SAMPLE_FACES)
    mock_store_detected_faces_to_db = Mock(return_value={})
    mock_store_detected_faces_images_to_disk = Mock(return_value=SAMPLE_FACES)

    monkeypatch.setattr(
        "fm_face.jobs.extract_faces_from_image.get_uploaded_file_path",
        mock_get_uploaded_file_path,
    )
    monkeypatch.setattr(
        "fm_face.jobs.extract_faces_from_image.detect_faces_from_image",
        mock_detect_faces_from_image,
    )
    monkeypatch.setattr(
        "fm_face.jobs.extract_faces_from_image.store_detected_faces_to_db",
        mock_store_detected_faces_to_db,
    )
    monkeypatch.setattr(
        "fm_face.jobs.extract_faces_from_image."
        "store_detected_faces_images_to_processed_folder",
        mock_store_detected_faces_images_to_disk,
    )

    faces = extract_faces_from_image.apply(args=(image.uuid,)).get()

    mock_get_uploaded_file_path.assert_called_once_with(image.storage_name)
    mock_detect_faces_from_image.assert_called_once_with(SAMPLE_IMAGE_PATH)
    mock_store_detected_faces_to_db.assert_called_once_with(
        SAMPLE_FACES, parent=image
    )
    mock_store_detected_faces_images_to_disk.assert_called_once_with(
        SAMPLE_FACES
    )

    assert faces == {}


def test_store_PIL_Image_as_jpeg_in_processed_folder(client, monkeypatch):
    """
    GIVEN a PIL.Image.Image object
    WHEN the image file is stored in the processed folder
    THEN check that the file is stored correctly and returns information about
         the processed image
    """
    filename = "01.jpeg"
    mock_generate_random_filename = Mock(return_value=filename)
    mock_os_path_getsize = Mock(return_value=666)

    monkeypatch.setattr(
        "fm_face.modules.image.services.generate_random_filename",
        mock_generate_random_filename,
    )
    monkeypatch.setattr(
        "fm_face.modules.image.services.os.path.getsize",
        mock_os_path_getsize,
    )

    file_path = get_sample_image_path(filename)
    test_image = PIL.Image.open(file_path)
    processed_image_info = store_PIL_Image_as_jpeg_in_processed_folder(
        test_image
    )
    processed_image = PIL.Image.open(processed_image_info["file_path"])

    assert processed_image.format == "JPEG"
    assert processed_image_info["size"] == 666
    assert processed_image_info["width"] == 259
    assert processed_image_info["height"] == 194
    assert processed_image_info["file_name"] == filename
    assert no_image_pixel_differences(processed_image, test_image)

    mock_generate_random_filename.assert_called_once_with(extension="jpg")
    mock_os_path_getsize.assert_called_once_with(
        processed_image_info["file_path"]
    )


def test_store_processed_image_info_to_db(client):
    """
    GIVEN the processed image info
    WHEN the processed image info is stored to the database
    THEN check that the file info is stored correctly and return the image
         model object
    """
    image = store_processed_image_info_to_db(PROCESSED_IMAGE_INFO)
    assert image == Image.query.first()
    assert image.size == PROCESSED_IMAGE_INFO["size"]
    assert image.width == PROCESSED_IMAGE_INFO["width"]
    assert image.height == PROCESSED_IMAGE_INFO["height"]
    assert image.name == PROCESSED_IMAGE_INFO["file_name"]
    assert image.storage_name == PROCESSED_IMAGE_INFO["file_name"]


def test_detect_faces_from_image(client, monkeypatch):
    """
    GIVEN the image path
    WHEN faces are detected from the image
    THEN check that faces are detected correctly and return the image
         info about the faces
    """

    mock_PIL_Image_crop = Mock(return_value="crop")
    mock_PIL_Image_open = Mock(return_value=SAMPLE_PIL_IMAGE)
    mock_RetinaFace_detect_faces = Mock(return_value=SAMPLE_FACES)

    monkeypatch.setattr(
        "fm_face.modules.image.services.RetinaFace.detect_faces",
        mock_RetinaFace_detect_faces,
    )
    monkeypatch.setattr(
        "fm_face.modules.image.services.PIL.Image.open",
        mock_PIL_Image_open,
    )
    monkeypatch.setattr(
        "fm_face.modules.image.services.PIL.Image.Image.crop",
        mock_PIL_Image_crop,
    )

    detected_faces = detect_faces_from_image(SAMPLE_IMAGE_PATH)

    mock_PIL_Image_crop.assert_has_calls(
        [
            call(tuple(SAMPLE_FACES["face_1"]["facial_area"])),
            call(tuple(SAMPLE_FACES["face_2"]["facial_area"])),
        ]
    )
    mock_PIL_Image_open.assert_called_once_with(SAMPLE_IMAGE_PATH)
    mock_RetinaFace_detect_faces.assert_called_with(SAMPLE_IMAGE_PATH)

    for face_id, face_info in detected_faces.items():
        assert face_info["PIL_image"] == "crop"
        assert face_info["score"] == SAMPLE_FACES[face_id]["score"]
        assert face_info["facial_area"] == SAMPLE_FACES[face_id]["facial_area"]


def test_store_detected_faces_images_to_processed_folder(client, monkeypatch):
    """
    GIVEN the detected faces dict
    WHEN the object is stored to the processed folder
    THEN check that faces are stored correctly and return info about the faces
    """
    sample_detected_faces = SAMPLE_FACES.copy()

    for face_id, face_info in sample_detected_faces.items():
        sample_detected_faces[face_id].update({"PIL_image": SAMPLE_PIL_IMAGE})

    mock_store_PIL_Image_as_jpeg_in_processed_folder = Mock(
        return_value=PROCESSED_IMAGE_INFO
    )

    monkeypatch.setattr(
        "fm_face.modules.image.services."
        "store_PIL_Image_as_jpeg_in_processed_folder",
        mock_store_PIL_Image_as_jpeg_in_processed_folder,
    )

    faces = store_detected_faces_images_to_processed_folder(
        sample_detected_faces
    )

    mock_store_PIL_Image_as_jpeg_in_processed_folder.assert_called_with(
        SAMPLE_PIL_IMAGE
    )

    for face_id, face_info in faces.items():
        assert face_info["score"] == SAMPLE_FACES[face_id]["score"]
        assert face_info["facial_area"] == SAMPLE_FACES[face_id]["facial_area"]
        assert face_info["image_info"] == PROCESSED_IMAGE_INFO


def test_store_detected_faces_image_info_to_db(client, monkeypatch):
    """
    GIVEN the detected faces dict
    WHEN the object is stored to the database
    THEN check that images info are stored correctly
    """
    sample_detected_faces = SAMPLE_FACES.copy()

    for face_id, face_info in sample_detected_faces.items():
        sample_detected_faces[face_id].update(
            {"image_info": PROCESSED_IMAGE_INFO}
        )

    mock_store_processed_image_info_to_db = Mock(return_value="image")

    monkeypatch.setattr(
        "fm_face.modules.image.services.store_processed_image_info_to_db",
        mock_store_processed_image_info_to_db,
    )

    faces = store_detected_faces_image_info_to_db(sample_detected_faces)

    mock_store_processed_image_info_to_db.assert_called_with(
        PROCESSED_IMAGE_INFO
    )

    for face_id, face_info in faces.items():
        assert face_info["image"] == "image"
        assert face_info["score"] == SAMPLE_FACES[face_id]["score"]
        assert face_info["facial_area"] == SAMPLE_FACES[face_id]["facial_area"]
        assert face_info["image_info"] == PROCESSED_IMAGE_INFO


def test_store_detected_faces_to_db(client, monkeypatch):
    """
    GIVEN the detected faces dict
    WHEN the object is stored to the database
    THEN check that face info are stored correctly and returns a list of face
         dicts
    """
    run_image_seeder()

    images = Image.query.all()
    face_image = images[0]
    parent_image = images[1]

    sample_detected_faces = SAMPLE_FACES.copy()

    for face_id, face_info in sample_detected_faces.items():
        sample_detected_faces[face_id].update({"image": face_image})

    faces = store_detected_faces_to_db(sample_detected_faces, parent_image)

    assert len(Face.query.all()) == 2
    for face in faces:
        face_dao = Face.query.get(face["uuid"])
        sample_face_dict = None
        for sample_face in sample_detected_faces.values():
            if sample_face["score"] == face_dao.score:
                sample_face_dict = sample_face

        assert face_dao.uuid == face["uuid"]
        assert face_dao.score == face["score"]
        assert face_dao.uuid == face["uuid"]
        assert face_dao.image_uuid == face["image_uuid"]
        assert face_dao.parent_uuid == face["parent_uuid"]
        assert face_dao.facial_area.x1 == face["facial_area"]["x1"]
        assert face_dao.facial_area.y1 == face["facial_area"]["y1"]
        assert face_dao.facial_area.x2 == face["facial_area"]["x2"]
        assert face_dao.facial_area.y2 == face["facial_area"]["y2"]
        assert face_dao.image == face_image
        assert face_dao.parent == parent_image
        assert face_dao.facial_area.x1 == sample_face_dict["facial_area"][0]
        assert face_dao.facial_area.y1 == sample_face_dict["facial_area"][1]
        assert face_dao.facial_area.x2 == sample_face_dict["facial_area"][2]
        assert face_dao.facial_area.y2 == sample_face_dict["facial_area"][3]
