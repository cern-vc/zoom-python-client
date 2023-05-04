import pytest
import responses

from tests.zoom_python_client.base_test_case import TestCaseWithAuth
from zoom_python_client.client_components.webinar_livestreams.webinar_livestreams_component import (
    WebinarLiveStreamsComponent,
)
from zoom_python_client.zoom_api_client import ZoomApiClient
from zoom_python_client.zoom_auth_api.zoom_auth_api_client import ZoomAuthApiClientError


class TestWebinarLiveStreamsComponent(TestCaseWithAuth):
    @responses.activate
    def test_get_webinar_livestreams_component(self):
        responses.add(
            responses.GET,
            "http://localhost/webinars/12345/livestream",
            json={"response": "ok"},
            status=200,
        )
        zoom_client = ZoomApiClient("aaa", "bbb", "ccc", "http://localhost")
        component = WebinarLiveStreamsComponent(zoom_client)
        user = component.get_livestream("12345")
        assert user == {"response": "ok"}

    @responses.activate
    def test_get_webinar_livestreams_component_empty_response(self):
        responses.add(
            responses.GET,
            "http://localhost/webinars/12345/livestream",
            status=200,
        )
        zoom_client = ZoomApiClient("aaa", "bbb", "ccc", "http://localhost")
        component = WebinarLiveStreamsComponent(zoom_client)
        with pytest.raises(
            ZoomAuthApiClientError,
            match="Webinar livestream must have been configured in advance",
        ):
            component.get_livestream("12345")

    @responses.activate
    def test_update_webinar_livestreams_component(self):
        responses.add(
            responses.PATCH,
            "http://localhost/webinars/12345/livestream",
            json={"response": "ok"},
            status=204,
        )
        zoom_client = ZoomApiClient("aaa", "bbb", "ccc", "http://localhost")
        component = WebinarLiveStreamsComponent(zoom_client)
        result = component.update_livestream(
            "12345",
            {
                "page_url": "https://example.com/livestream/123",
                "stream_key": "contact-it@example.com",
                "stream_url": "https://example.com/livestream",
            },
        )
        assert result

    @responses.activate
    def test_update_webinar_livestreams_component_no_response(self):
        responses.add(
            responses.PATCH,
            "http://localhost/webinars/12345/livestream",
            json={"response": "ok"},
            status=200,
        )
        zoom_client = ZoomApiClient("aaa", "bbb", "ccc", "http://localhost")
        component = WebinarLiveStreamsComponent(zoom_client)
        result = component.update_livestream(
            "12345",
            {
                "page_url": "https://example.com/livestream/123",
                "stream_key": "contact-it@example.com",
                "stream_url": "https://example.com/livestream",
            },
        )
        assert not result

    @responses.activate
    def test_update_webinar_livestreams_status_component(self):
        responses.add(
            responses.PATCH,
            "http://localhost/webinars/12345/livestream/status",
            json={"response": "ok"},
            status=204,
        )
        zoom_client = ZoomApiClient("aaa", "bbb", "ccc", "http://localhost")
        component = WebinarLiveStreamsComponent(zoom_client)
        result = component.update_livestream_status("12345", "start")
        assert result

    @responses.activate
    def test_update_webinar_livestreams_status_component_no_response(self):
        responses.add(
            responses.PATCH,
            "http://localhost/webinars/12345/livestream/status",
            json={"response": "ok"},
            status=200,
        )
        zoom_client = ZoomApiClient("aaa", "bbb", "ccc", "http://localhost")
        component = WebinarLiveStreamsComponent(zoom_client)
        result = component.update_livestream_status("12345", "start")
        assert not result
