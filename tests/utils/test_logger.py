import logging

from zoom_python_client.utils.logger import setup_logs


def test_setup_logs():
    logger = setup_logs(log_level=logging.DEBUG)

    assert logger is not None
