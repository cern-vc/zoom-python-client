import logging
import os

from zoom_python_client.utils.logger import setup_logs
from zoom_python_client.zoom_api_client import ZoomApiClient

zoom_client = ZoomApiClient.init_from_dotenv()
setup_logs(log_level=logging.DEBUG)
USER_ID = os.environ["USER_ID"]
result = zoom_client.users.get_user(USER_ID)
print(result)
