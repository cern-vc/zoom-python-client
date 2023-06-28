import logging

from typing_extensions import TypedDict

logger = logging.getLogger("python_zoom_client")


class DataType(TypedDict, total=False):
    ...


def generate_parms_dict(data: DataType) -> dict:
    """Generate a dictionary of parameters to be used in the API request.

    Args:
        data (TypedDict): The parameters to be used in the API request.

    Returns:
        dict: The parameters to be used in the API request.
    """

    parameters = {}
    for key, value in data.items():
        if value is not None:
            parameters[key] = value

    logger.debug(f"Parameters: {parameters}")
    return parameters
