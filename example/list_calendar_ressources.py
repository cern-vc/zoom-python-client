import logging

from zoom_python_client.utils.logger import setup_logs
from zoom_python_client.zoom_api_client import ZoomApiClient

logger = setup_logs(log_level=logging.DEBUG)

zoom_client = ZoomApiClient.init_from_dotenv(use_path=".")


result = zoom_client.calendars.list_calendar_resources()

logger.info("Found %d calendars:", len(result))

for calendar_ressources in result:
    logger.info(
        "\t- %s - %s - %s",
        calendar_ressources["calendar_resource_name"],
        calendar_ressources["calendar_resource_id"],
        calendar_ressources["calendar_resource_email"],
    )
