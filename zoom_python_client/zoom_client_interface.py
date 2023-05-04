import logging
from abc import ABC, abstractmethod
from typing import Any, Mapping

import requests

logger = logging.getLogger("python_zoom_client")


class ZoomClientInterface(ABC):
    @abstractmethod
    def make_get_request(
        self, api_path: str, parameters: dict = {}
    ) -> requests.Response:
        logger.warning("Method not implemented")
        raise NotImplementedError

    @abstractmethod
    def make_post_request(
        self, api_path: str, data: Mapping[str, Any]
    ) -> requests.Response:
        logger.warning("Method not implemented")
        raise NotImplementedError

    @abstractmethod
    def make_patch_request(
        self, api_path: str, data: Mapping[str, Any]
    ) -> requests.Response:
        logger.warning("Method not implemented")
        raise NotImplementedError
