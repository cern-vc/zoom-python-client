import logging
import os
from typing import Any, Mapping

import requests
from dotenv import load_dotenv

from zoom_python_client.api_client import ApiClient
from zoom_python_client.client_components.meeting_livestreams.meeting_livestreams_component import (
    MeetingLiveStreamsComponent,
)
from zoom_python_client.client_components.meetings.meetings_component import (
    MeetingsComponent,
)
from zoom_python_client.client_components.users.users_component import UsersComponent
from zoom_python_client.client_components.webinar_livestreams.webinar_livestreams_component import (
    WebinarLiveStreamsComponent,
)
from zoom_python_client.client_components.webinars.webinars_component import (
    WebinarsComponent,
)
from zoom_python_client.utils.file_system import get_project_dir
from zoom_python_client.zoom_auth_api.zoom_auth_api_client import ZoomAuthApiClient
from zoom_python_client.zoom_client_interface import ZoomClientInterface

# This goes into your library somewhere
logging.getLogger("zoom_python_client").addHandler(logging.NullHandler())

logger = logging.getLogger("zoom_python_client")


class ZoomClientEnvError(Exception):
    pass


class ZoomClientError(Exception):
    pass


class ZoomApiClient(ZoomClientInterface):
    api_endpoint: str = "https://api.zoom.us/v2"

    @staticmethod
    def init_from_env(log_level=logging.WARNING):
        try:
            account_id = os.environ["ZOOM_ACCOUNT_ID"]
            client_id = os.environ["ZOOM_CLIENT_ID"]
            client_secret = os.environ["ZOOM_CLIENT_SECRET"]
            zoom_client = ZoomApiClient(account_id, client_id, client_secret)
            return zoom_client
        except KeyError as error:
            raise ZoomClientEnvError(
                f"Required key not in environment: {error}"
            ) from error

    @staticmethod
    def init_from_dotenv(log_level=logging.WARNING, custom_dotenv=".env"):
        project_dir = get_project_dir()
        load_dotenv(os.path.join(project_dir, custom_dotenv), verbose=True)
        zoom_client = ZoomApiClient.init_from_env(log_level)
        return zoom_client

    def init_components(self):
        # Add all the new components here
        self.users = UsersComponent(self)
        self.meetings = MeetingsComponent(self)
        self.meeting_livestreams = MeetingLiveStreamsComponent(self)
        self.webinars = WebinarsComponent(self)
        self.webinar_livestreams = WebinarLiveStreamsComponent(self)

    def __init__(
        self,
        account_id: str,
        client_id: str,
        client_secret: str,
        api_endpoint="https://api.zoom.us/v2",
    ):
        self.api_endpoint = api_endpoint
        self.api_client = ApiClient(self.api_endpoint)
        self.authentication_client = ZoomAuthApiClient(
            account_id, client_id, client_secret
        )

        # Initialize components
        self.init_components()

    def build_zoom_authorization_headers(self, force_token=False) -> dict:
        access_token = os.getenv("ZOOM_ACCESS_TOKEN", default=None)
        expire_seconds = os.getenv("ZOOM_ACCESS_TOKEN_EXPIRE", default=None)
        if (
            not access_token
            or not expire_seconds
            or self.authentication_client.is_zoom_access_token_expired()
            or force_token
        ):
            access_token = self.authentication_client.get_acceess_token()

        zoom_headers = {"Authorization": "Bearer " + access_token}
        headers = self.api_client.build_headers(extra_headers=zoom_headers)
        return headers

    def build_query_string_from_dict(self, parameters: dict) -> str:
        query_string = "?"
        for key, value in parameters.items():
            if value:
                query_string += f"{key}={value}&"
        return query_string

    def make_get_request(
        self, api_path: str, parameters: dict = {}
    ) -> requests.Response:
        headers = self.build_zoom_authorization_headers()
        # convert parameters dict to query string
        query_string = self.build_query_string_from_dict(parameters)
        response = requests.Response()
        try:
            response = self.api_client.make_get_request(
                api_path + query_string, headers=headers
            )
        except requests.exceptions.HTTPError as error:
            logger.warning(f"Error from Zoom on GET request: {error}")
            if error.response.status_code == 401:
                logger.warning(f"Building headers again. Error: {error}")
                headers = self.build_zoom_authorization_headers(force_token=True)
                response = self.api_client.make_get_request(
                    api_path + query_string, headers=headers
                )
        return response

    def make_post_request(
        self, api_path: str, data: Mapping[str, Any]
    ) -> requests.Response:
        headers = self.build_zoom_authorization_headers()
        response = requests.Response()
        try:
            response = self.api_client.make_post_request(
                api_path, headers=headers, data=data
            )
        except requests.exceptions.HTTPError as error:
            logger.warning(f"Error from Zoom on POST request: {error}")
            if error.response.status_code == 401:
                logger.warning(f"Building headers again for POST. Error: {error}")
                headers = self.build_zoom_authorization_headers(force_token=True)
                response = self.api_client.make_post_request(
                    api_path, headers=headers, data=data
                )

        return response

    def make_patch_request(
        self, api_path: str, data: Mapping[str, Any]
    ) -> requests.Response:
        headers = self.build_zoom_authorization_headers()
        response = requests.Response()

        try:
            response = self.api_client.make_patch_request(
                api_path, headers=headers, data=data
            )
        except requests.exceptions.HTTPError as error:
            logger.warning(f"Error from Zoom on PATCH request: {error}")

            if error.response.status_code == 401:
                logger.warning(f"Building headers again for PATCH. Error: {error}")
                headers = self.build_zoom_authorization_headers()
                response = self.api_client.make_patch_request(
                    api_path, headers=headers, data=data
                )
        return response
