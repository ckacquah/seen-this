from flask import Blueprint, jsonify

from app.modules.uploaded_images_handler.models import File
from app.tasks import celery
from app.tasks.demo import demo

uploaded_images_handler = Blueprint(
    'uploaded-images-handler', __name__, url_prefix='/uploaded-images-handler')


@uploaded_images_handler.route('/')
def index():
    task = demo.apply_async(args=["tempt-temp-temp"])
    return jsonify({"task_id": task.id})


@uploaded_images_handler.route('/task/<task_id>')
def task(task_id, methods=['GET']):
    print(task_id)
    task_result = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200


@uploaded_images_handler.route('/images')
def images():
    return jsonify([{'id': 1, 'name': 'image1'}, {'id': 2, 'name': 'image2'}])
