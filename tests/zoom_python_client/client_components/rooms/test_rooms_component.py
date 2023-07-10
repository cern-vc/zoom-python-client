import pytest
import responses

from tests.zoom_python_client.base_test_case import TestCaseWithAuth
from zoom_python_client.client_components.rooms.rooms_component import (
    RoomsComponent,
    RoomsSensorDataDict,
)
from zoom_python_client.zoom_api_client import ZoomApiClient


class TestRoomsComponent(TestCaseWithAuth):
    def setUp(self):
        super().setUp()
        zoom_client = ZoomApiClient("aaa", "bbb", "ccc", "http://localhost")
        self.rooms_component = RoomsComponent(zoom_client)

    @responses.activate
    def test_get_rooms(self):
        responses.add(
            responses.GET,
            "http://localhost/rooms",
            json={"response": "ok"},
            status=200,
        )
        rooms = self.rooms_component.get_rooms({})
        assert rooms == {"response": "ok"}

    @responses.activate
    def test_get_room(self):
        responses.add(
            responses.GET,
            "http://localhost/rooms/12345",
            json={"response": "ok"},
            status=200,
        )
        room = self.rooms_component.get_room("12345")
        assert room == {"response": "ok"}

    @responses.activate
    def test_get_room_sensor_data_0(self):
        responses.add(
            responses.GET,
            "http://localhost/rooms/12345/sensor_data",
            json={"response": "ok"},
            status=200,
        )
        parameters = RoomsSensorDataDict(
            from_date="2020-01-01",
            to_date="2023-07-10T08:27:46Z",
        )
        with pytest.raises(ValueError):
            self.rooms_component.get_room_sensor_data("12345", parameters)

    @responses.activate
    def test_get_room_sensor_data_1(self):
        responses.add(
            responses.GET,
            "http://localhost/rooms/12345/sensor_data",
            json={"response": "ok"},
            status=200,
        )
        parameters = RoomsSensorDataDict(
            from_date="2023-07-10T08:27:46Z",
            to_date="2020-01-01",
        )
        with pytest.raises(ValueError):
            self.rooms_component.get_room_sensor_data("12345", parameters)

    @responses.activate
    def test_get_room_sensor_data_2(self):
        responses.add(
            responses.GET,
            "http://localhost/rooms/12345/sensor_data",
            json={"response": "ok"},
            status=200,
        )
        parameters = RoomsSensorDataDict(
            from_date="2023-07-10T08:27:46Z",
            to_date="2023-07-10T10:27:46Z",
        )
        result = self.rooms_component.get_room_sensor_data("12345", parameters)
        assert result == {"response": "ok"}
