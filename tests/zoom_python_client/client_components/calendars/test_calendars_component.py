import pytest
import responses

from tests.zoom_python_client.base_test_case import TestCaseWithAuth
from zoom_python_client.client_components.calendars.calendars_component import (
    CalendarsComponent,
)
from zoom_python_client.zoom_api_client import ZoomApiClient


class TestCalendarsComponent(TestCaseWithAuth):
    def setUp(self):
        super().setUp()
        zoom_client = ZoomApiClient("aaa", "bbb", "ccc", "http://localhost")
        self.calendars_component = CalendarsComponent(zoom_client)

    @responses.activate
    def test_list_calendar_services(self):
        responses.add(
            responses.GET,
            "http://localhost/rooms/calendar/services",
            json={"response": "ok"},
            status=200,
        )
        calendar_services = self.calendars_component.list_calendar_services()
        assert calendar_services == {"response": "ok"}

    @responses.activate
    def test_list_calendar_resources(self):
        responses.add(
            responses.GET,
            "http://localhost/rooms/calendar/services",
            json={"calendar_services": [{"calendar_service_id": "12345"}]},
            status=200,
        )
        responses.add(
            responses.GET,
            "http://localhost/rooms/calendar/services/12345/resources",
            json={"calendar_resources": [{"calendar_resource_id": "12345"}]},
            status=200,
        )
        calendar_resources = self.calendars_component.list_calendar_resources()
        assert calendar_resources == [{"calendar_resource_id": "12345"}]

    @responses.activate
    def test_list_calendar_resources_by_service_id(self):
        responses.add(
            responses.GET,
            "http://localhost/rooms/calendar/services/12345/resources",
            json={"response": "ok"},
            status=200,
        )
        calendar_resources = (
            self.calendars_component.list_calendar_resources_by_service_id("12345")
        )
        assert calendar_resources == {"response": "ok"}

    @responses.activate
    def test_get_calendar_resource_by_ressource_id(self):
        responses.add(
            responses.GET,
            "http://localhost/rooms/calendar/services",
            json={"calendar_services": [{"calendar_service_id": "12345"}]},
            status=200,
        )
        responses.add(
            responses.GET,
            "http://localhost/rooms/calendar/services/12345/resources",
            json={"calendar_resources": [{"calendar_resource_id": "12345"}]},
            status=200,
        )
        calendar_resource = (
            self.calendars_component.get_calendar_resource_by_ressource_id("12345")
        )
        assert calendar_resource == {"calendar_resource_id": "12345"}

    @responses.activate
    def test_get_calendar_resource_by_ressource_id_not_found(self):
        responses.add(
            responses.GET,
            "http://localhost/rooms/calendar/services",
            json={"calendar_services": [{"calendar_service_id": "12345"}]},
            status=200,
        )
        responses.add(
            responses.GET,
            "http://localhost/rooms/calendar/services/12345/resources",
            json={"calendar_resources": [{"calendar_resource_id": "12345"}]},
            status=200,
        )
        with pytest.raises(ValueError):
            self.calendars_component.get_calendar_resource_by_ressource_id("123456")
