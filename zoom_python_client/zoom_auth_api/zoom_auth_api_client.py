import logging
import os
from base64 import b64encode
from time import time
from typing import Optional

from zoom_python_client.api_client import ApiClient

logger = logging.getLogger("zoom_python_client")


class ZoomAuthApiClientError(Exception):
    pass


class ZoomAuthApiClient:
    oauth_base_url: str = "https://zoom.us/oauth"
    minimum_expire_time_seconds: int = 300

    def __init__(
        self,
        account_id: str,
        client_id: str,
        client_secret: str,
        use_path: Optional[str] = None,
    ):
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.authentication_client = ApiClient(self.oauth_base_url)
        self.use_path = use_path

    def base64_encode_auth(self):
        encoded_auth = b64encode(
            bytes(f"{self.client_id}:{self.client_secret}", "utf-8")
        ).decode()
        return encoded_auth

    def is_zoom_access_token_expired(self, expire_seconds):
        current_seconds = int(time())

        if expire_seconds:
            expire_seconds_int = int(expire_seconds)
            remaining_seconds = expire_seconds_int - current_seconds
            logger.debug(f"Remaining seconds: {remaining_seconds}")
            if remaining_seconds > self.minimum_expire_time_seconds:
                return False
        logger.debug("Access token is expired")
        return True

    def generate_auth_headers(self):
        encoded_auth = self.base64_encode_auth()
        authentication_headers = {"Authorization": f"Basic {encoded_auth}"}
        headers = self.authentication_client.build_headers(
            extra_headers=authentication_headers
        )
        logger.debug("Auth headers generated")
        return headers

    def save_token_and_seconds_to_env(self, result):
        try:
            os.environ["ZOOM_ACCESS_TOKEN"] = result["access_token"]
            os.environ["ZOOM_ACCESS_TOKEN_EXPIRE"] = str(
                int(time()) + int(result["expires_in"])
            )
        except ValueError as error:
            raise ZoomAuthApiClientError(
                "Unable to set access_token expiration. expires_in is not an int"
            ) from error

    def save_token_and_seconds_to_file(self, result):
        # Save the token to a file
        if self.use_path is None:
            raise ZoomAuthApiClientError("use_path is None")
        file_path = os.path.join(self.use_path, "access_token")
        with open(file_path, "w") as token_file:
            token_file.write(result["access_token"])
        # Save the expire_seconds to a file
        file_path = os.path.join(self.use_path, "expire_seconds")
        with open(file_path, "w") as token_file:
            new_expire = str(int(time()) + int(result["expires_in"]))
            token_file.write(new_expire)
        return True

    def extract_access_token(self, result):
        if "access_token" in result and "expires_in" in result:
            if self.use_path:
                self.save_token_and_seconds_to_file(result)
            else:
                self.save_token_and_seconds_to_env(result)
            logger.debug("Access token extracted from oauth response")
            return result["access_token"]

        raise ZoomAuthApiClientError("Unable to get access_token")

    def get_acceess_token(self):
        api_path = f"/token?grant_type=account_credentials&account_id={self.account_id}"

        headers = self.generate_auth_headers()
        response = self.authentication_client.make_post_request(
            api_path, headers=headers
        )
        result = response.json()
        access_token = self.extract_access_token(result)
        return access_token

    def get_access_token_from_file(self):
        if self.use_path is None:
            raise ZoomAuthApiClientError("use_path is None")
        # join the path to the file name
        file_path = os.path.join(self.use_path, "access_token")
        try:
            with open(file_path, "r") as token_file:
                access_token = token_file.read()
                return access_token
        except FileNotFoundError:
            return None

    def get_expire_seconds_from_file(self):
        # join the path to the file name
        if self.use_path is None:
            raise ZoomAuthApiClientError("use_path is None")
        file_path = os.path.join(self.use_path, "expire_seconds")
        try:
            with open(file_path, "r") as token_file:
                access_token = token_file.read()
                return access_token
        except FileNotFoundError:
            return None
