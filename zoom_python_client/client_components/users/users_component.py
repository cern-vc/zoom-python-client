from typing_extensions import NotRequired, TypedDict

from zoom_python_client.zoom_client_interface import ZoomClientInterface


class MeetingsListDict(TypedDict):
    type: NotRequired[str]
    page_size: NotRequired[int]
    page_number: NotRequired[int]
    next_page_token: NotRequired[str]
    from_date: NotRequired[str]
    to_date: NotRequired[str]


class UsersComponent:
    def __init__(self, client: ZoomClientInterface) -> None:
        self.client = client

    def get_user(self, user_id: str) -> dict:
        api_path = f"/users/{user_id}"
        response = self.client.make_get_request(api_path)
        result = response.json()
        return result

    def get_user_meetings(self, user_id: str, data: MeetingsListDict) -> dict:
        api_path = f"/users/{user_id}/meetings/"

        parameters = {
            "type": data.get("type", None),
            "page_size": data.get("page_size", None),
            "next_page_token": data.get("next_page_token", None),
            "page_number": data.get("page_number", None),
            "from": data.get("from_date", None),
            "to": data.get("to_date", None),
        }

        response = self.client.make_get_request(api_path, parameters=parameters)
        result = response.json()
        return result
