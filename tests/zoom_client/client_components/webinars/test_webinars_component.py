import responses
from tests.zoom_client.base_test_case import TestCaseWithAuth
from zoom_client.zoom_api_client import ZoomApiClient
from zoom_client.client_components.webinars.webinars_component import WebinarsComponent


class TestWebinarsComponent(TestCaseWithAuth):
    @responses.activate
    def test_meetings_component(self):
        responses.add(
            responses.GET,
            "http://localhost/webinars/12345",
            json={"response": "ok"},
            status=200,
        )
        zoom_client = ZoomApiClient("aaa", "bbb", "ccc", "http://localhost")
        component = WebinarsComponent(zoom_client)
        user = component.get_webinar("12345")
        assert user == {"response": "ok"}
