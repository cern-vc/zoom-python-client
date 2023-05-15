import logging
import os
import time

from zoom_python_client.client_components.meeting_livestreams.meeting_livestreams_component import (
    LiveStreamDict,
)
from zoom_python_client.utils.logger import setup_logs
from zoom_python_client.zoom_api_client import ZoomApiClient

setup_logs(log_level=logging.DEBUG)
zoom_client = ZoomApiClient.init_from_dotenv()
MEETING_ID = os.environ["MEETING_ID"]
STREAM_URL = os.environ["STREAM_URL"]

data: LiveStreamDict = {
    "page_url": "https://home.cern",
    "stream_url": STREAM_URL,
    "stream_key": MEETING_ID,
    "resolution": "720p",
}


# time.sleep(1)
# result = zoom_client.meeting_livestreams.update_livestream_status(MEETING_ID, "stop")
# print(result)

time.sleep(1)
result = zoom_client.meeting_livestreams.update_livestream(MEETING_ID, data)
print(result)

# time.sleep(1)
# result = zoom_client.meeting_livestreams.update_livestream_status(MEETING_ID, "start")
# print(result)
