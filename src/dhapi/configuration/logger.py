import logging
import sys


def set_logger(debug=False):
    root_logger = logging.getLogger()

    if debug:
        sys.tracebacklimit = 1000
        root_logger.setLevel(logging.DEBUG)
    else:
        sys.tracebacklimit = 0  # suppress traceback
        root_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(stream=sys.stdout)
    root_logger.addHandler(handler)

    def handle_exception(exc_type, exc_value, exc_traceback):
        # skip capturing intentional exit by Ctrl-c
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        root_logger.debug("🚨 full exception context:", exc_info=(exc_type, exc_value, exc_traceback))
        root_logger.error("🚨 에러가 발생했습니다: %s", exc_value)

    sys.excepthook = handle_exception
