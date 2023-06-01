from pathlib import Path


def get_project_dir():
    return Path(__file__).resolve().parents[2]
