import logging
import os

from zoom_python_client.zoom_api_client import ZoomApiClient

USER_ID = os.environ["USER_ID"]
zoom_client = ZoomApiClient.init_from_dotenv(logging.DEBUG)


result = zoom_client.users.get_user(USER_ID)
print(result)
