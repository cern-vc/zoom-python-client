import logging

from zoom_python_client.client_components.rooms.rooms_component import (
    RoomsListDict,
    RoomType,
)
from zoom_python_client.utils.logger import setup_logs
from zoom_python_client.zoom_api_client import ZoomApiClient

logger = setup_logs(log_level=logging.INFO)

zoom_client = ZoomApiClient.init_from_dotenv(use_path=".")

parameters = RoomsListDict(
    type=RoomType.ZOOM_ROOM,
)

rooms = zoom_client.rooms.get_rooms(parameters)

logger.info("Found %d rooms:", len(rooms["rooms"]))
for room in rooms["rooms"]:
    room_profile = zoom_client.rooms.get_room(room["id"])

    calendar_ressource = zoom_client.calendars.get_calendar_resource_by_ressource_id(
        room_profile["basic"]["calendar_resource_id"]
    )

    logger.info(
        "\t- Microsoft user id for room %s is %s",
        room["name"],
        calendar_ressource["calendar_resource_email"],
    )
