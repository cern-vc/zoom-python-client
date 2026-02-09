import logging
import os

from zoom_python_client.utils.logger import setup_logs
from zoom_python_client.zoom_api_client import ZoomApiClient

setup_logs(log_level=logging.DEBUG)
zoom_client = ZoomApiClient.init_from_dotenv()
MEETING_ID = os.environ["MEETING_ID"]


result = zoom_client.meeting_livestreams.get_livestream(MEETING_ID)
print(result)

settings = {
    "active_speaker_name": False,
    "display_name": "CERN_Webcast_Service",
    "layout": "follow_host",
    "close_caption": "embedded",
}
started = zoom_client.meeting_livestreams.update_livestream_status(
    MEETING_ID,
    "start",
    settings=settings,
)
print(started)
