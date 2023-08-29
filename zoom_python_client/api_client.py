import json
import logging

import requests

logger = logging.getLogger("zoom_python_client")


class ApiClient:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url

    def build_headers(self, extra_headers=None) -> dict:
        """Create the headers for a request appending the ones in the params

        Args:
            extra_headers (dict): Dict of headers that will be appended to the default ones

        Returns:
            dict: All the headers
        """
        headers = {"Content-type": "application/json"}
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def make_get_request(self, api_path: str, headers: dict) -> requests.Response:
        """Makes a GET request using requests

        Args:
            api_path (str): The URL path
            headers (dict): The headers of the request

        Returns:
            dict: A JSON dict
        """
        full_url = self.api_base_url + api_path
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        return response

    def make_post_request(
        self, api_path: str, data=None, headers=None
    ) -> requests.Response:
        """Makes a POST request using requests

        Args:
            api_path (str): The URL path
            data (_type_, optional): The form body. Defaults to None.
            headers (_type_, optional): The request headers. Defaults to None.

        Returns:
            dict: A JSON dict
        """
        full_url = self.api_base_url + api_path
        response = requests.post(full_url, headers=headers, data=data)
        response.raise_for_status()
        return response

    def make_patch_request(
        self, api_path: str, data=None, headers=None
    ) -> requests.Response:
        """Makes a PATCH request using requests

        Args:
            api_path (str): The URL path
            data (_type_, optional): The form body. Defaults to None.
            headers (_type_, optional): The request headers. Defaults to None.

        Returns:
            dict: A JSON dict
        """
        full_url = self.api_base_url + api_path
        response = requests.patch(full_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response
