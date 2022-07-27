from api.utils.testing.faker import generate_fake_images
from api.modules.image.schemas import image_schema, images_schema


def test_image_schema():
    """
    GIVEN a Image object
    WHEN the object is dumped
    THEN check that the dictionary is valid
    """
    image = generate_fake_images(1)[0]
    image_dict = image_schema.dump(image)

    assert image_dict["uuid"] == image.uuid
    assert image_dict["name"] == image.name
    assert image_dict["size"] == image.size
    assert image_dict["width"] == image.width
    assert image_dict["height"] == image.height
    assert image_dict["source"] == image.source
    assert image_dict["storage_name"] == image.storage_name
    assert image_dict["created_at"] == image.created_at
    assert image_dict["updated_at"] == image.updated_at


def test_image_schemas():
    """
    GIVEN a list of Image objects
    WHEN the list is dumped
    THEN check that the results is valid
    """
    images = generate_fake_images(3)
    images_list = images_schema.dump(images)

    for image_dict, image in zip(images_list, images):
        assert image_dict["uuid"] == image.uuid
        assert image_dict["name"] == image.name
        assert image_dict["size"] == image.size
        assert image_dict["width"] == image.width
        assert image_dict["height"] == image.height
        assert image_dict["source"] == image.source
        assert image_dict["storage_name"] == image.storage_name
        assert image_dict["created_at"] == image.created_at
        assert image_dict["updated_at"] == image.updated_at
