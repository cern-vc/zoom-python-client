import re
from enum import Enum

from typing_extensions import NotRequired, TypedDict

from zoom_python_client.utils.typed_dict_parameters import generate_parameters_dict
from zoom_python_client.zoom_client_interface import ZoomClientInterface


class RoomStatus(Enum):
    OFFLINE = "Offline"
    AVAILABLE = "Available"
    IN_MEETING = "InMeeting"
    UNDER_CONSTRUCTION = "UnderConstruction"


class RoomType(Enum):
    KIOSK = "Kiosk"
    ZOOM_ROOM = "ZoomRoom"
    STANDALONE_WHITEBOARD = "StandaloneWhiteboard"
    SCHEDULING_DISPLAY_ONLY = "SchedulingDisplayOnly"
    DIGITAL_SIGNAGE_ONLY = "DigitalSignageOnly"


class NewPageToken(TypedDict):
    """The parameters for queries that return paginated results.

    Args:
        next_page_token (str): The token for the next page of results.
        page_size (int): The number of records returned with a single API call.
    """

    next_page_token: NotRequired[str]
    page_size: NotRequired[int]


class RoomsListDict(NewPageToken):
    """The parameters for the get_rooms method.

    Args:
        status (Status): The status of the room.
        type (Type): The type of the room.
        unassigned_rooms (bool): Whether or not to include unassigned rooms.
        location_id (str): The location ID of the room.
        query_name (str): The name of the room.
    """

    status: NotRequired[RoomStatus]
    type: NotRequired[RoomType]
    unassigned_rooms: NotRequired[bool]
    location_id: NotRequired[str]
    query_name: NotRequired[str]


class RoomsSensorDataDict(NewPageToken):
    """The parameters for the get_sensor_data method.

    Args:
        from_date (str): The start date and time for the query, should be in yyyy-MM-ddTHH:dd:ssZ format
        to_date (str): The end date and time for the query, should be in yyyy-MM-ddTHH:dd:ssZ format
    """

    from_date: str
    to_date: str


class RoomsComponent:
    def __init__(self, client: ZoomClientInterface) -> None:
        self.client = client

    def get_rooms(self, data: RoomsListDict) -> dict:
        api_path = "/rooms"
        parameters = generate_parameters_dict(data)

        response = self.client.make_get_request(api_path, parameters=parameters)
        result = response.json()
        return result

    def get_room(self, room_id: str) -> dict:
        api_path = f"/rooms/{room_id}"

        response = self.client.make_get_request(api_path)
        result = response.json()
        return result

    def get_room_sensor_data(self, room_id: str, data: RoomsSensorDataDict) -> dict:
        api_path = f"/rooms/{room_id}/sensor_data"

        # Validate the date format
        regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"  # yyyy-MM-ddTHH:dd:ssZ
        if not (
            re.match(regex, data["from_date"]) and re.match(regex, data["to_date"])
        ):
            raise ValueError("The date format should be in yyyy-MM-ddTHH:dd:ssZ format")

        parameters = generate_parameters_dict(data)

        response = self.client.make_get_request(api_path, parameters=parameters)
        result = response.json()
        return result
