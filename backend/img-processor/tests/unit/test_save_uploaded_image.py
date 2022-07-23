import os
import PIL

from app.utils import get_uploaded_file_path
from app.utils.testing import get_sample_image_path, sample_images
from app.modules.image.services import save_uploaded_image


def test_save_uploaded_image(client):
    """
    GIVEN a file's name and its content
    WHEN an image file is saved
    THEN check that the image is valid and return information about
         the image file stored on disk
    """
    filename = sample_images[0]
    file_path = get_sample_image_path(filename)
    with open(file_path, mode="rb") as image_file:
        saved_image = save_uploaded_image(
            name=filename, content=image_file.read()
        )
    image_path = get_uploaded_file_path(saved_image["storage_name"])
    image = PIL.Image.open(image_path)
    assert image.format == "JPEG"
    assert saved_image["name"] == filename
    assert saved_image["source"] == "upload"
    # check if the file extension is .jpg
    assert saved_image["storage_name"].split(".")[-1] == "jpg"
    assert saved_image["size"] == os.path.getsize(image_path)
    assert saved_image["width"], saved_image["height"] == image.size
