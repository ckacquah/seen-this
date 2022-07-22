import os
import io
import PIL

from app.base_model import db
from app.utils import generate_random_filename, get_uploaded_file_path, allowed_file
from app.modules.image.models import Image
from app.modules.image.schemas import image_schema


def save_uploaded_image(name, content):
    try:
        image = PIL.Image.open(io.BytesIO(content))
        storage_name = generate_random_filename("jpg")
        storage_path = get_uploaded_file_path(storage_name)
        image.save(storage_path)
        size = os.path.getsize(storage_path)
        width, height = image.size
        image_dao = Image(
            name=name,
            source="upload",
            size=size,
            width=width,
            height=height,
            storage_name=storage_name,
        )
        db.session.add(image_dao)
        db.session.commit()
        return image_schema.dump(image_dao)
    except PIL.UnidentifiedImageError:
        pass
