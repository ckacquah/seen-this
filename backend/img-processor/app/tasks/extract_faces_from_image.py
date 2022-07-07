import os
import cv2
import json
from retinaface import RetinaFace

from app.tasks import celery, flask_app
from app.modules.image.models import db, File, Face, faces_schema
from app.utils import (
    get_uploaded_file_path,
    get_processed_face_path,
    generate_random_file_name,
)


@celery.task(name="extract-faces-from-image", bind=True)
def extract_faces_from_image(self, image_param):
    image_file = File.query.get(image_param["image"])
    image_path = get_uploaded_file_path(image_file.name)
    detected_faces = RetinaFace.detect_faces(image_path).values()
    extracted_faces = extract_faces_as_images(image_path, detected_faces)
    saved_faces = save_extracted_faces_to_storage(extracted_faces)
    faces = save_extracted_faces_to_db(saved_faces, image_file)
    return {"faces": faces}


def extract_faces_as_images(image_path, detected_faces):
    extracted_faces = []
    image = cv2.imread(image_path)
    for detected_face in detected_faces:
        x1, y1, x2, y2 = detected_face["facial_area"]
        extracted_faces.append(
            {
                "image": image[y1:y2, x1:x2],
                "score": detected_face["score"],
                "facial_area": detected_face["facial_area"],
            }
        )
    return extracted_faces


def save_extracted_faces_to_storage(extracted_faces):
    saved_faces = []
    for extracted_face in extracted_faces:
        file_name = generate_random_file_name(18) + ".jpeg"
        file_path = get_processed_face_path(file_name)
        cv2.imwrite(file_path, extracted_face["image"])
        saved_faces.append(
            {
                "file_name": file_name,
                "score": extracted_face["score"],
                "facial_area": extracted_face["facial_area"],
            }
        )
    return saved_faces


def save_extracted_faces_to_db(saved_faces, parent):
    files, faces = [], []
    for face in saved_faces:
        image_path = get_processed_face_path(face["file_name"])
        files.append(File(name=face["file_name"], size=os.path.getsize(image_path)))
        faces.append(Face(file=files[-1], parent=parent, score=face["score"]))
    db.session.add_all(files + faces)
    db.session.commit()
    return faces_schema.dump(faces)
