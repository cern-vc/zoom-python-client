import os
from base64 import b64encode
from pathlib import Path
import requests
from dotenv import load_dotenv


class ZoomClientError(Exception):
    pass


def get_project_dir():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    path = Path(current_dir)
    project_dir = path.parent.absolute()
    return project_dir


class ZoomClient:

    api_base_url: str = "https://api.zoom.us/v2"
    oauth_base_url: str = "https://zoom.us/oauth"

    @staticmethod
    def init_from_env():
        account_id = os.getenv("ZOOM_ACCOUNT_ID", default=None)
        client_id = os.getenv("ZOOM_CLIENT_ID", default=None)
        client_secret = os.getenv("ZOOM_CLIENT_SECRET", default=None)
        print(f"{account_id} - {client_id} - {client_secret}")
        if account_id and client_id and client_secret:
            zoom_client = ZoomClient(account_id, client_id, client_secret)
            return zoom_client
        raise ZoomClientError(
            "ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID or ZOOM_CLIENT_SECRET are not properly set in the environment variables"
        )

    @staticmethod
    def init_from_dotenv():
        project_dir = get_project_dir()
        load_dotenv(os.path.join(project_dir, ".env"), verbose=True)
        zoom_client = ZoomClient.init_from_env()
        return zoom_client

    def __init__(self, account_id: str, client_id: str, client_secret: str):
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret

    def get_acceess_token(self):
        api_path = f"/token?grant_type=account_credentials&account_id={self.account_id}"
        encoded_auth = b64encode(
            bytes(f"{self.client_id}:{self.client_secret}", "utf-8")
        ).decode()
        headers = {"Authorization": f"Basic {encoded_auth}"}
        full_url = self.oauth_base_url + api_path
        response = requests.post(full_url, headers=headers)
        result = response.json()

        if "access_token" in result:
            os.environ["ZOOM_ACCESS_TOKEN"] = result["access_token"]
            return result["access_token"]
        raise ZoomClientError("Unable to get access_token")

    def build_headers(self) -> dict:
        access_token = os.getenv("ZOOM_ACCESS_TOKEN", default=None)
        if not access_token:
            access_token = self.get_acceess_token()

        headers = {"Authorization": "Bearer " + access_token}
        return headers

    def make_get_request(self, api_path: str):
        headers = self.build_headers()
        full_url = self.api_base_url + api_path
        response = requests.get(full_url, headers=headers)
        result = response.json()
        return result

    def get_user(self, user_id: str):
        api_path = f"/users/{user_id}"
        result = self.make_get_request(api_path)
        print(result)
        return result
