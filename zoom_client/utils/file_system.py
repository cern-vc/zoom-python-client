import os
from pathlib import Path


def get_project_dir():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    path = Path(current_dir)
    project_dir = path.parent.absolute().parent
    return project_dir
