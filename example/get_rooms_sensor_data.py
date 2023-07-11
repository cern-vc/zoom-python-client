import datetime
import logging
import os
import sys

import pytz

from zoom_python_client.client_components.rooms.rooms_component import (
    RoomsSensorDataDict,
)
from zoom_python_client.utils.logger import setup_logs
from zoom_python_client.zoom_api_client import ZoomApiClient

logger = setup_logs(log_level=logging.DEBUG)

zoom_client = ZoomApiClient.init_from_dotenv(use_path=".")

ROOM_ID = os.getenv("ROOM_ID")

if ROOM_ID is None:
    logger.error("ROOM_ID not found in environment variables")
    sys.exit(1)


all_sensor_data = []

from_date = (datetime.datetime.now() - datetime.timedelta(hours=12)).isoformat(
    timespec="seconds"
) + "Z"
to_date = datetime.datetime.now().isoformat(timespec="seconds") + "Z"

room_params = RoomsSensorDataDict(
    from_date=from_date,
    to_date=to_date,
)

while True:
    result = zoom_client.rooms.get_room_sensor_data(ROOM_ID, data=room_params)
    all_sensor_data.extend(result["sensor_data"])
    if not result["next_page_token"]:
        break
    room_params["next_page_token"] = result["next_page_token"]

logger.info("Found %d sensor data points:", len(all_sensor_data))

for data in all_sensor_data:
    date = datetime.datetime.strptime(
        data["date_time"], "%Y-%m-%dT%H:%M:%SZ"
    ).astimezone(pytz.timezone("Europe/Zurich"))
    logger.info("\t-%s - %d", date, data["sensor_value"])
