import logging
import sys


def setup_logs(log_level=logging.WARNING):
    logger = logging.getLogger("zoom_python_client")

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s | %(pathname)s:%(lineno)d | %(funcName)s()"
    )

    configure_stdout_logging(logger=logger, formatter=formatter, log_level=log_level)

    return logger


def configure_stdout_logging(logger, formatter=None, log_level=logging.WARNING):
    stream_handler = logging.StreamHandler(stream=sys.stdout)

    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)

    logger.addHandler(stream_handler)
    print(f"Logging {str(logger)} to stdout -> True")
