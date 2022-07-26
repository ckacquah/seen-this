from api.base_model import ma


class FaceExtractionJobSchema(ma.Schema):
    class Meta:
        fields = (
            "uuid",
            "tag",
            "status",
            "image_uuid",
            "completion_time",
            "percentage_complete",
        )


face_extraction_job_schema = FaceExtractionJobSchema()
face_extraction_jobs_schema = FaceExtractionJobSchema(many=True)
