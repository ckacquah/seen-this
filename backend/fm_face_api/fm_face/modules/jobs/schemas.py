from fm_face.base_model import ma


class JobSchema(ma.Schema):
    class Meta:
        fields = (
            "uuid",
            "tag",
            "status",
            "percentage_complete",
            "completion_time",
        )


job_schema = JobSchema()
jobs_schema = JobSchema(many=True)
