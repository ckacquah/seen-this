import os
import PIL

from conftest import client

from app.utils import get_uploaded_file_path
from app.utils.testing import get_sample_image_path, sample_images
from app.modules.image.models import Image
from app.modules.image.schemas import image_schema
from app.modules.image.services import save_uploaded_image


def test_save_uploaded_image(client):
    for sample_image_name in sample_images:
        image_file = open(get_sample_image_path(sample_image_name), mode="rb")
        image_content = image_file.read()
        assert image_content is not None
        saved_image = save_uploaded_image(name=sample_image_name, content=image_content)
        assert saved_image["name"] == sample_image_name
        assert saved_image["source"] == "upload"
        assert saved_image["storage_name"] is not None
        # check if the file extension is .jpg
        assert saved_image["storage_name"].split(".")[-1] == "jpg"
        image_path = get_uploaded_file_path(saved_image["storage_name"])
        assert os.path.exists(image_path)
        assert saved_image["size"] == os.path.getsize(image_path)
        image = PIL.Image.open(image_path)
        assert image.format == "JPEG"
        assert (saved_image["width"], saved_image["height"]) == image.size
        assert image_schema.dump(Image.query.get(saved_image["uuid"])) == saved_image
