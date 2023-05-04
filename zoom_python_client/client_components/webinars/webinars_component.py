from zoom_python_client.zoom_client_interface import ZoomClientInterface


class WebinarsComponent:
    def __init__(self, client: ZoomClientInterface) -> None:
        self.client = client

    def get_webinar(self, webinar_id: str) -> dict:
        api_path = f"/webinars/{webinar_id}"
        response = self.client.make_get_request(api_path)
        result = response.json()
        return result
