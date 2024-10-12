import logging
import sys

def set_logger(is_debug):
    _log_level = logging.DEBUG if is_debug else logging.INFO

    logging.basicConfig(
        level=_log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[logging.StreamHandler()]  # Replace RichHandler with StreamHandler
    )
    sys.tracebacklimit = 1000 if is_debug else 0

    logging.debug(f"log level is set to {_log_level}, traceback limit is set to {sys.tracebacklimit}")
