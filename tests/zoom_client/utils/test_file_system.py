import os
from zoom_python_client.utils.file_system import get_project_dir


def test_get_project_dir():
    project_dir = get_project_dir()
    assert str(project_dir) == os.getcwd()
