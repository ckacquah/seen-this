import PIL
import pytest

from unittest.mock import Mock
from werkzeug.datastructures import FileStorage

from app.modules.image.models import Image
from app.utils.testing import (
    get_sample_file_path,
    get_sample_image_path,
    no_image_pixel_differences,
)
from app.modules.image.services import (
    ImageLoadError,
    save_uploaded_image,
    store_uploaded_image_info_to_db,
    convert_FileStorage_object_to_PIL_Image,
    store_PIL_Image_as_jpeg_in_uploads_folder,
)


def test_save_uploaded_image(client, monkeypatch):
    """
    GIVEN a werkzeug.datastructures.FileStorage object
    WHEN the uploaded image file is saved
    THEN check that the image is valid and return information about
         the uploaded image
    """
    mock_convert_FileStorage_object_to_PIL_Image = Mock(return_value=1)
    mock_store_PIL_Image_as_jpeg_in_uploads_folder = Mock(return_value={})
    mock_store_uploaded_image_info_to_db = Mock(return_value=2)
    mock_secure_filename = Mock(return_value="name.jpg")

    monkeypatch.setattr(
        "app.modules.image.services.convert_FileStorage_object_to_PIL_Image",
        mock_convert_FileStorage_object_to_PIL_Image,
    )
    monkeypatch.setattr(
        "app.modules.image.services.store_PIL_Image_as_jpeg_in_uploads_folder",
        mock_store_PIL_Image_as_jpeg_in_uploads_folder,
    )
    monkeypatch.setattr(
        "app.modules.image.services.store_uploaded_image_info_to_db",
        mock_store_uploaded_image_info_to_db,
    )
    monkeypatch.setattr(
        "app.modules.image.services.secure_filename",
        mock_secure_filename,
    )

    file_path = get_sample_image_path("01.jpeg")
    with open(file_path, mode="rb") as f:
        file_storage_object = FileStorage(f, filename="01.jpeg")
        uploaded_image_info = save_uploaded_image(file_storage_object)

    assert uploaded_image_info == 2

    mock_convert_FileStorage_object_to_PIL_Image.assert_called_once_with(
        file_storage_object
    )
    mock_store_PIL_Image_as_jpeg_in_uploads_folder.assert_called_once_with(1)
    mock_store_uploaded_image_info_to_db.assert_called_once_with(
        {"name": "name.jpg"}
    )
    mock_secure_filename.assert_called_once_with("01.jpeg")


def test_convert_FileStorage_object_to_PIL_Image():
    """
    GIVEN a werkzeug.datastructures.FileStorage object
    WHEN the object is converted to PIL.Image.Image
    THEN check that the object contains a  valid image and return a
         PIL.ImageFile.ImageFile object created from the object
    """
    file_path = get_sample_image_path("01.jpeg")
    with open(file_path, mode="rb") as f:
        file_storage_object = FileStorage(f)
        image = convert_FileStorage_object_to_PIL_Image(file_storage_object)
    assert isinstance(image, PIL.Image.Image)
    assert image.format == "JPEG"


def test_convert_FileStorage_object_to_PIL_Image_with_invalid_file():
    """
    GIVEN a werkzeug.datastructures.FileStorage object
    WHEN the object is converted to PIL.Image.Image
    THEN ImageLoadError exception is raised
    """
    file_path = get_sample_file_path("sample.txt")
    with open(file_path, mode="rb") as f:
        file_storage_object = FileStorage(f)
        with pytest.raises(ImageLoadError) as error:
            convert_FileStorage_object_to_PIL_Image(file_storage_object)
        assert "Failed to open image" in str(error.value)


def test_store_PIL_Image_as_jpeg_in_uploads_folder(client, monkeypatch):
    """
    GIVEN a PIL.Image.Image object
    WHEN the image file is stored in the upload_folder
    THEN check that the file is stored correctly and returns information about
        the uploaded image
    """
    mock_generate_random_filename = Mock(return_value="file_name.jpg")
    mock_os_path_getsize = Mock(return_value=666)

    monkeypatch.setattr(
        "app.modules.image.services.generate_random_filename",
        mock_generate_random_filename,
    )
    monkeypatch.setattr(
        "app.modules.image.services.os.path.getsize",
        mock_os_path_getsize,
    )

    file_path = get_sample_image_path("01.jpeg")
    test_image = PIL.Image.open(file_path)
    uploaded_image_info = store_PIL_Image_as_jpeg_in_uploads_folder(test_image)
    uploaded_image = PIL.Image.open(uploaded_image_info["file_path"])

    assert uploaded_image_info["file_name"] == "file_name.jpg"
    assert uploaded_image_info["size"] == 666
    assert uploaded_image_info["width"] == 259
    assert uploaded_image_info["height"] == 194
    assert uploaded_image.format == "JPEG"
    assert no_image_pixel_differences(uploaded_image, test_image)

    mock_generate_random_filename.assert_called_once_with(extension="jpg")
    mock_os_path_getsize.assert_called_once_with(
        uploaded_image_info["file_path"]
    )


def test_store_uploaded_image_info_to_db(client, monkeypatch):
    """
    GIVEN a uploaded image info
    WHEN the store the information on the disk
    THEN check that the file info is stored correctly and return the image
         info as a dict
    """
    uploaded_image_info = {
        "name": "name.jpg",
        "size": 666,
        "width": 666,
        "height": 666,
        "file_name": "file_name.jpg",
    }
    image_info = store_uploaded_image_info_to_db(uploaded_image_info)
    image = Image.query.first()
    assert image_info["uuid"] == image.uuid
    assert image_info["source"] == image.source == "upload"
    assert image_info["name"] == uploaded_image_info["name"] == image.name
    assert image_info["size"] == uploaded_image_info["size"] == image.size
    assert image_info["width"] == uploaded_image_info["width"] == image.width
    assert (
        image_info["height"] == uploaded_image_info["height"] == image.height
    )
    assert (
        image_info["storage_name"]
        == uploaded_image_info["file_name"]
        == image.storage_name
    )
