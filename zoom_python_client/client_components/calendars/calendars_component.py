from typing import Any

from zoom_python_client.zoom_client_interface import ZoomClientInterface


class CalendarsComponent:
    def __init__(self, client: ZoomClientInterface) -> None:
        self.client = client

    def list_calendar_services(self) -> dict:
        api_path = "/rooms/calendar/services"
        response = self.client.make_get_request(api_path)
        result = response.json()
        return result

    def list_calendar_resources(self) -> list[Any]:
        calendar_services = self.list_calendar_services()
        calendar_service_ids = [
            calendar_service["calendar_service_id"]
            for calendar_service in calendar_services["calendar_services"]
        ]
        calendar_resources = []
        for calendar_service_id in calendar_service_ids:
            res = self.list_calendar_resources_by_service_id(calendar_service_id)
            for resource in res["calendar_resources"]:
                calendar_resources.append(resource)

        return calendar_resources

    def list_calendar_resources_by_service_id(self, calendar_service_id: str) -> dict:
        api_path = f"/rooms/calendar/services/{calendar_service_id}/resources"
        response = self.client.make_get_request(api_path)
        result = response.json()
        return result

    def get_calendar_resource_by_ressource_id(self, resource_id: str) -> dict:
        all_ressources = self.list_calendar_resources()
        for resource in all_ressources:
            if resource["calendar_resource_id"] == resource_id:
                return resource

        raise ValueError(f"Resource with id {resource_id} not found")
