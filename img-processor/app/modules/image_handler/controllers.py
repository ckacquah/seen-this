import os
import uuid
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER
from app.tasks import celery
from app.tasks.demo import demo
from app.modules.image_handler.models import File

image_handler = Blueprint(
    'images', __name__, url_prefix='/images')


@image_handler.route('/')
def index():
    task = demo.apply_async(args=["tempt-temp-temp"])
    return jsonify({"task_id": task.id})


@image_handler.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']

    destination_path = os.path.join(
        UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(destination_path)

    return jsonify({
        "message": "Image uploaded successfully",
        "image_name": file.filename
    }), 200


@image_handler.route('/task/<task_id>')
def task(task_id, methods=['GET']):
    print(task_id)
    task_result = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200
