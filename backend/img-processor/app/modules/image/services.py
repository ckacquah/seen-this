import os
import io
import PIL
import imghdr

from retinaface import RetinaFace
from werkzeug.utils import secure_filename

from app.base_model import db
from app.modules.face.models import Face, FacialArea
from app.modules.face.schemas import faces_schema
from app.modules.image.models import Image
from app.modules.image.schemas import image_schema
from app.utils import (
    is_allowed_image_name,
    get_uploaded_file_path,
    get_processed_file_path,
    generate_random_filename,
)


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


def store_PIL_Image_as_jpeg_in_processed_folder(PIL_image):
    processed_image_width, processed_image_height = PIL_image.size
    processed_file_name = generate_random_filename(extension="jpg")
    processed_file_path = get_processed_file_path(processed_file_name)
    PIL_image.save(processed_file_path)
    processed_file_size = os.path.getsize(processed_file_path)
    return {
        "size": processed_file_size,
        "width": processed_image_width,
        "height": processed_image_height,
        "file_name": processed_file_name,
        "file_path": processed_file_path,
    }


def store_PIL_Image_as_jpeg_in_uploads_folder(PIL_image):
    uploaded_image_width, uploaded_image_height = PIL_image.size
    uploaded_file_name = generate_random_filename(extension="jpg")
    uploaded_file_path = get_uploaded_file_path(uploaded_file_name)
    PIL_image.save(uploaded_file_path)
    uploaded_file_size = os.path.getsize(uploaded_file_path)
    return {
        "size": uploaded_file_size,
        "width": uploaded_image_width,
        "height": uploaded_image_height,
        "file_name": uploaded_file_name,
        "file_path": uploaded_file_path,
    }


def store_processed_image_info_to_db(processed_image_info):
    image = Image(
        source="processed",
        size=processed_image_info["size"],
        width=processed_image_info["width"],
        height=processed_image_info["height"],
        name=processed_image_info["file_name"],
        storage_name=processed_image_info["file_name"],
    )
    db.session.add(image)
    db.session.commit()
    return image


def store_uploaded_image_info_to_db(uploaded_image_info):
    image = Image(
        source="upload",
        name=uploaded_image_info["name"],
        size=uploaded_image_info["size"],
        width=uploaded_image_info["width"],
        height=uploaded_image_info["height"],
        storage_name=uploaded_image_info["file_name"],
    )
    db.session.add(image)
    db.session.commit()
    return image_schema.dump(image)


def detect_faces_from_image(image_path):
    PIL_image = PIL.Image.open(image_path)
    detected_faces = RetinaFace.detect_faces(image_path)
    for face_id, detected_face_info in detected_faces.items():
        detected_faces[face_id].update(
            {
                "PIL_image": PIL_image.crop(
                    tuple(detected_face_info["facial_area"])
                )
            }
        )
    return detected_faces


def store_detected_faces_images_to_processed_folder(detected_faces):
    for face_id, detected_face_info in detected_faces.items():
        detected_faces[face_id].update(
            {
                "image_info": store_PIL_Image_as_jpeg_in_processed_folder(
                    detected_face_info["PIL_image"]
                )
            }
        )
    return detected_faces


def store_detected_faces_image_info_to_db(detected_faces):
    for face_id, detected_face_info in detected_faces.items():
        detected_faces[face_id].update(
            {
                "image": store_processed_image_info_to_db(
                    detected_face_info["image_info"]
                )
            }
        )
    return detected_faces


def store_detected_faces_to_db(detected_faces, parent):
    faces = [
        Face(
            parent=parent,
            file=detected_face["image"],
            score=detected_face["score"],
            facial_area=FacialArea(
                x1=detected_face["facial_area"][0],
                y1=detected_face["facial_area"][1],
                x2=detected_face["facial_area"][2],
                y2=detected_face["facial_area"][3],
            ),
        )
        for detected_face in detected_faces.values()
    ]
    db.session.add_all(faces)
    db.session.commit()
    return faces_schema.dump(faces)
