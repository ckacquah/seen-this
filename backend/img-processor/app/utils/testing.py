import os

from app.config.testing import TestingConfig

config = TestingConfig()

UPLOAD_FOLDER = config.UPLOAD_FOLDER
SAMPLES_FOLDER = config.SAMPLES_FOLDER
PROCESSED_FACES_FOLDER = config.PROCESSED_FACES_FOLDER

sample_images = ["01.jpeg", "02.jpeg", "03.jpeg", "04.jpeg", "05.jpeg"]


def delete_processed_files():
    filelist = os.listdir(PROCESSED_FACES_FOLDER)
    for f in filelist:
        os.remove(os.path.join(PROCESSED_FACES_FOLDER, f))


def delete_uploaded_files():
    filelist = os.listdir(UPLOAD_FOLDER)
    for f in filelist:
        if f != ".gitignore":
            os.remove(os.path.join(UPLOAD_FOLDER, f))


def get_sample_image_path(filename):
    return os.path.join(SAMPLES_FOLDER, "images", filename)


def get_sample_file_path(filename):
    return os.path.join(SAMPLES_FOLDER, "files", filename)


def upload_image(client, image_name):
    image_path = get_sample_image_path(image_name)
    with open(image_path, "rb") as img:
        response = client.post(
            "image/upload", data={"image": (img, image_name)}
        )
    return response


def upload_images(client, images=sample_images):
    for image in images:
        upload_image(client, image)
