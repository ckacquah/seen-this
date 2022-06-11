from flask import Blueprint, jsonify

from app.modules.uploaded_images_handler.models import File

uploaded_images_handler = Blueprint(
    'uploaded-images-handler', __name__, url_prefix='/uploaded-images-handler')


@uploaded_images_handler.route('/')
def index():
    return "It works!"


@uploaded_images_handler.route('/images')
def images():
    return jsonify([{'id': 1, 'name': 'image1'}, {'id': 2, 'name': 'image2'}])
