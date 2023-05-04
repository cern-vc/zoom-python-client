import responses

from tests.zoom_python_client.base_test_case import TestCaseWithAuth
from zoom_python_client.client_components.users.users_component import UsersComponent
from zoom_python_client.zoom_api_client import ZoomApiClient


class TestUsersComponent(TestCaseWithAuth):
    @responses.activate
    def test_get_user(self):
        responses.add(
            responses.GET,
            "http://localhost/users/12345",
            json={"response": "ok"},
            status=200,
        )
        zoom_client = ZoomApiClient("aaa", "bbb", "ccc", "http://localhost")
        users_component = UsersComponent(zoom_client)
        user = users_component.get_user("12345")
        assert user == {"response": "ok"}

    @responses.activate
    def test_get_user_meetings(self):
        responses.add(
            responses.GET,
            "http://localhost/users/12345/meetings/",
            json={"response": "ok"},
            status=200,
        )
        zoom_client = ZoomApiClient("aaa", "bbb", "ccc", "http://localhost")
        users_component = UsersComponent(zoom_client)
        user = users_component.get_user_meetings("12345", {})
        assert user == {"response": "ok"}
