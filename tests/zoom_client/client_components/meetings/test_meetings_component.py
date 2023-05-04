import responses
from tests.zoom_python_client.base_test_case import TestCaseWithAuth
from zoom_python_client.zoom_api_client import ZoomApiClient
from zoom_python_client.client_components.meetings.meetings_component import (
    MeetingsComponent,
)


class TestMeetingsComponent(TestCaseWithAuth):
    @responses.activate
    def test_meetings_component(self):
        responses.add(
            responses.GET,
            "http://localhost/meetings/12345",
            json={"response": "ok"},
            status=200,
        )
        zoom_client = ZoomApiClient("aaa", "bbb", "ccc", "http://localhost")
        component = MeetingsComponent(zoom_client)
        user = component.get_meeting("12345")
        assert user == {"response": "ok"}
