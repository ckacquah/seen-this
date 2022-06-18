import pytest

from marshmallow import Schema, fields, ValidationError
from app.modules.image_handler.schemas import ExtractFacesFromImagesRequestSchema


def test_valid_extract_faces_from_image_request_schema():
    assert (
        ExtractFacesFromImagesRequestSchema().load(
            {
                "backend": "retinaface",
                "targets": [
                    "6c75bcc8-0419-45de-b820-3960e683d859",
                    "b38f4df5-f047-4c6e-8760-765bf1c0a659",
                ],
            }
        )
        != None
    )


def test_error_with_missing_backend_in_extract_faces_request_schema():
    with pytest.raises(ValidationError):
        ExtractFacesFromImagesRequestSchema().load(
            {
                "targets": [
                    "6c75bcc8-0419-45de-b820-3960e683d859",
                    "b38f4df5-f047-4c6e-8760-765bf1c0a659",
                ],
            }
        )


def test_error_with_missing_targets_in_extract_faces_request_schema():
    with pytest.raises(ValidationError):
        ExtractFacesFromImagesRequestSchema().load(
            {
                "backend": "retinaface",
            }
        )


def test_error_with_invalid_backends_in_extract_faces_request_schema():
    with pytest.raises(ValidationError):
        ExtractFacesFromImagesRequestSchema().load(
            {
                "backend": "invalid",
                "targets": [
                    "6c75bcc8-0419-45de-b820-3960e683d859",
                    "b38f4df5-f047-4c6e-8760-765bf1c0a659",
                ],
            }
        )
