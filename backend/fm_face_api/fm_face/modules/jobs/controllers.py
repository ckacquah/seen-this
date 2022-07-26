from flask import Blueprint, jsonify

from fm_face.modules.jobs.models import FaceExtractionJob
from fm_face.modules.jobs.schemas import face_extraction_job_schema

extraction_jobs_blueprint = Blueprint(
    "extraction-jobs", __name__, url_prefix="/extraction-jobs"
)


@extraction_jobs_blueprint.route("/<job_id>", methods=["GET"])
def get_extraction_job_by_id(job_id):
    job = FaceExtractionJob.query.get(job_id)
    if job is None:
        return jsonify({"message": "Extraction job not found"}), 404
    return jsonify(face_extraction_job_schema.dump(job)), 200
