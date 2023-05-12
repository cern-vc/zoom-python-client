import logging
import os

from zoom_python_client.client_components.users.users_component import MeetingsListDict
from zoom_python_client.utils.logger import setup_logs
from zoom_python_client.zoom_api_client import ZoomApiClient

setup_logs(log_level=logging.DEBUG)
zoom_client = ZoomApiClient.init_from_dotenv()
USER_ID = os.environ["USER_ID"]


data: MeetingsListDict = {
    # "type": "scheduled",
    # "page_size": 30,
    # "page_number": 1,
    # "from_date": "2021-01-01",
    # "to_date": "2021-12-31",
    # "next_page_token": "",
}

result = zoom_client.users.get_user_meetings(
    USER_ID,
    data,
)
print(result)
