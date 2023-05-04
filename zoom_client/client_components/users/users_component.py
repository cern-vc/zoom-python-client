from zoom_client.zoom_client_interface import ZoomClientInterface


class UsersComponent:
    def __init__(self, client: ZoomClientInterface) -> None:
        self.client = client

    def get_user(self, user_id: str) -> dict:
        api_path = f"/users/{user_id}"
        response = self.client.make_get_request(api_path)
        result = response.json()
        return result
