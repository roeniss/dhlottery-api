import logging
import sys


def set_logger(is_debug=False):
    root_logger = logging.getLogger()

    sys.tracebacklimit = 1000

    if is_debug:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(stream=sys.stdout)
    root_logger.addHandler(handler)

    def handle_exception(exc_type, exc_value, exc_traceback):
        # skip capturing intentional exit by Ctrl-c
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        root_logger.error("🚨 예상치 못한 에러가 발생했습니다.")
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    sys.excepthook = handle_exception
