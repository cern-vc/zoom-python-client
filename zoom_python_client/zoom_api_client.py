import logging
import os
from typing import Any, Mapping, Optional, Union

import requests
from dotenv import load_dotenv

from zoom_python_client.api_client import ApiClient
from zoom_python_client.client_components.meeting_livestreams.meeting_livestreams_component import (
    MeetingLiveStreamsComponent,
)
from zoom_python_client.client_components.meetings.meetings_component import (
    MeetingsComponent,
)
from zoom_python_client.client_components.rooms.rooms_component import RoomsComponent
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
    def init_from_env(use_path: Optional[str] = None):
        try:
            account_id = os.environ["ZOOM_ACCOUNT_ID"]
            client_id = os.environ["ZOOM_CLIENT_ID"]
            client_secret = os.environ["ZOOM_CLIENT_SECRET"]
            zoom_client = ZoomApiClient(
                account_id, client_id, client_secret, use_path=use_path
            )
            return zoom_client
        except KeyError as error:
            raise ZoomClientEnvError(
                f"Required key not in environment: {error}"
            ) from error

    @staticmethod
    def init_from_dotenv(
        custom_dotenv=".env",
        use_path: Optional[str] = None,
    ):
        project_dir = get_project_dir()
        load_dotenv(os.path.join(project_dir, custom_dotenv), verbose=True)
        zoom_client = ZoomApiClient.init_from_env(use_path=use_path)
        return zoom_client

    def init_components(self):
        # Add all the new components here
        self.users = UsersComponent(self)
        self.meetings = MeetingsComponent(self)
        self.meeting_livestreams = MeetingLiveStreamsComponent(self)
        self.webinars = WebinarsComponent(self)
        self.webinar_livestreams = WebinarLiveStreamsComponent(self)
        self.rooms = RoomsComponent(self)

    def __init__(
        self,
        account_id: str,
        client_id: str,
        client_secret: str,
        api_endpoint="https://api.zoom.us/v2",
        use_path: Optional[str] = None,
    ):
        self.api_endpoint = api_endpoint
        self.use_path = use_path
        self.api_client = ApiClient(self.api_endpoint)
        self.authentication_client = ZoomAuthApiClient(
            account_id, client_id, client_secret, use_path=use_path
        )

        # Initialize components
        self.init_components()

    def load_access_token_and_expire_seconds(self):
        if self.use_path:
            logger.debug("Loading token from file")
            # If the token is in a file, we need to get the token from the file
            access_token = self.authentication_client.get_access_token_from_file()
            expire_seconds = self.authentication_client.get_expire_seconds_from_file()
        else:
            logger.debug("Loading token from environment")
            access_token = os.getenv("ZOOM_ACCESS_TOKEN", default=None)
            expire_seconds = os.getenv("ZOOM_ACCESS_TOKEN_EXPIRE", default=None)
        return access_token, expire_seconds

    def build_zoom_authorization_headers(self, force_token=False) -> dict:
        access_token, expire_seconds = self.load_access_token_and_expire_seconds()
        token_from = "file" if self.use_path else "environment"
        if (
            not access_token
            or not expire_seconds
            or self.authentication_client.is_zoom_access_token_expired(expire_seconds)
            or force_token
        ):
            if force_token:
                logger.debug("Forcing token refresh")
            else:
                logger.debug(f"Token is not in the {token_from}. Requesting new token.")
            access_token = self.authentication_client.get_acceess_token()
        else:
            logger.debug(f"The token is the {token_from}. No need for a new token.")
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
    ) -> Union[requests.Response, None]:
        headers = self.build_zoom_authorization_headers()
        # convert parameters dict to query string
        query_string = self.build_query_string_from_dict(parameters)
        response = requests.Response()
        try:
            response = self.api_client.make_get_request(
                api_path + query_string, headers=headers
            )
        # Handle 401 error from requests
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 401:
                logger.debug(
                    f"Got 401 error from Zoom API Get ({error}). Retrying with a new token."
                )
                response = self.retry_get_request(api_path, query_string)
        return response

    def retry_get_request(self, api_path, query_string):
        headers = self.build_zoom_authorization_headers(force_token=True)
        response = self.api_client.make_get_request(
            api_path + query_string, headers=headers
        )

        return response

    def make_post_request(
        self, api_path: str, data: Mapping[str, Any]
    ) -> Union[requests.Response, None]:
        headers = self.build_zoom_authorization_headers()
        response = requests.Response()
        try:
            response = self.api_client.make_post_request(
                api_path, headers=headers, data=data
            )
        # Handle 401 error from requests
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 401:
                logger.debug(
                    f"Got 401 error from Zoom API Post ({error}). Retrying with a new token."
                )
                response = self.retry_post_request(api_path, data)

        return response

    def retry_post_request(self, api_path, data):
        headers = self.build_zoom_authorization_headers(force_token=True)
        response = self.api_client.make_post_request(
            api_path, headers=headers, data=data
        )

        return response

    def make_patch_request(
        self, api_path: str, data: Mapping[str, Any]
    ) -> Union[requests.Response, None]:
        headers = self.build_zoom_authorization_headers()
        response = requests.Response()
        try:
            response = self.api_client.make_patch_request(
                api_path, headers=headers, data=data
            )
        # Handle 401 error from requests
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 401:
                # Retry generating a new token
                logger.debug(
                    f"Got 401 error from Zoom API Patch ({error}). Retrying with a new token."
                )
                response = self.retry_patch_request(api_path, data)
        return response

    def retry_patch_request(self, api_path, data):
        headers = self.build_zoom_authorization_headers(force_token=True)
        response = self.api_client.make_patch_request(
            api_path, headers=headers, data=data
        )

        return response
