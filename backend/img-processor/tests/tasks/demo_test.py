import pytest
from app.tasks.demo import demo


def test_demo_task():
    assert demo.run(1)
