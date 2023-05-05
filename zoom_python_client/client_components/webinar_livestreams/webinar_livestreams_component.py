from json import JSONDecodeError
from typing import TypedDict

from zoom_python_client.zoom_auth_api.zoom_auth_api_client import ZoomAuthApiClientError
from zoom_python_client.zoom_client_interface import ZoomClientInterface


class LiveStreamDict(TypedDict):
    stream_url: str
    stream_key: str
    page_url: str
    resolution: str


class LiveStreamStatusDict(TypedDict):
    action: str


class WebinarLiveStreamsComponent:
    def __init__(self, client: ZoomClientInterface) -> None:
        self.client = client

    def get_livestream(self, meeting_id: str) -> dict:
        api_path = f"/webinars/{meeting_id}/livestream"
        response = self.client.make_get_request(api_path)
        try:
            result = response.json()
        except JSONDecodeError as error:
            raise ZoomAuthApiClientError(
                "Webinar livestream must have been configured in advance"
            ) from error
        return result

    def update_livestream(self, meeting_id: str, data: LiveStreamDict) -> bool:
        api_path = f"/webinars/{meeting_id}/livestream"
        response = self.client.make_patch_request(api_path, data)
        if response.status_code == 204:
            return True
        return False

    def update_livestream_status(self, meeting_id: str, action: str) -> bool:
        api_path = f"/webinars/{meeting_id}/livestream/status"
        data: LiveStreamStatusDict = {"action": action}
        response = self.client.make_patch_request(api_path, data)
        if response.status_code == 204:
            return True
        return False
