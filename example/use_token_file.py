import logging
import os

from dotenv import load_dotenv

from zoom_python_client.utils.file_system import get_project_dir
from zoom_python_client.utils.logger import setup_logs
from zoom_python_client.zoom_api_client import ZoomApiClient

project_dir = get_project_dir()
load_dotenv(os.path.join(project_dir, ".env"), verbose=True)

TEST_PATH = os.environ["TEST_PATH"]

zoom_client = ZoomApiClient.init_from_dotenv(from_path=TEST_PATH)
setup_logs(log_level=logging.DEBUG)
USER_ID = os.environ["USER_ID"]
result = zoom_client.users.get_user(USER_ID)
print(result)
