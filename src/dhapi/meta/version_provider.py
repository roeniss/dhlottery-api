from importlib.metadata import version
import logging


PACKAGE_NAME = "dhapi"

logger = logging.getLogger(__name__)


def get_installed_version():
    try:
        return version(PACKAGE_NAME)
    except Exception as e:
        logger.debug(e)
        return "Failed to load version. Use -d flag for debugging."
