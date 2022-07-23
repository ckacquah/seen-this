import os
import io
import PIL
import imghdr

from werkzeug.utils import secure_filename

from app.base_model import db
from app.utils import (
    generate_random_filename,
    get_uploaded_file_path,
    is_allowed_image_name,
)
from app.modules.image.models import Image
from app.modules.image.schemas import image_schema


def save_uploaded_image(file_storage_object):
    try:
        PIL_image = convert_FileStorage_object_to_PIL_Image(
            file_storage_object
        )
        uploaded_file_info = store_PIL_Image_as_jpeg_in_uploads_folder(
            PIL_image
        )
        uploaded_file_info.update(
            {"name": secure_filename(file_storage_object.filename)}
        )
        uploaded_image_info = store_uploaded_image_info_to_db(
            uploaded_file_info
        )
        return uploaded_image_info
    except ImageLoadError:
        return


class ImageLoadError(Exception):
    pass


def convert_FileStorage_object_to_PIL_Image(file_storage_object):
    file_stream = file_storage_object.stream
    if (
        is_allowed_image_name(file_storage_object.filename)
        and imghdr.what(file_stream) is not None
    ):
        file_stream.seek(0)  # Reset the stream to the start of the file
        return PIL.Image.open(io.BytesIO(file_stream.read()))

    raise ImageLoadError("Failed to open image")


def store_PIL_Image_as_jpeg_in_uploads_folder(image):
    uploaded_image_width, uploaded_image_height = image.size
    uploaded_file_name = generate_random_filename(extension="jpg")
    uploaded_file_path = get_uploaded_file_path(uploaded_file_name)
    image.save(uploaded_file_path)
    uploaded_file_size = os.path.getsize(uploaded_file_path)
    return {
        "size": uploaded_file_size,
        "width": uploaded_image_width,
        "height": uploaded_image_height,
        "file_name": uploaded_file_name,
        "file_path": uploaded_file_path,
    }


def store_uploaded_image_info_to_db(uploaded_image_info):
    image = Image(
        name=uploaded_image_info["name"],
        source="upload",
        size=uploaded_image_info["size"],
        width=uploaded_image_info["width"],
        height=uploaded_image_info["height"],
        storage_name=uploaded_image_info["file_name"],
    )
    db.session.add(image)
    db.session.commit()
    return image_schema.dump(image)
