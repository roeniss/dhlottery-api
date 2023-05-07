import sys
from dhapi.purchase.lotto645_controller import Lotto645Controller
from dhapi.router.arg_parser import ArgParser
from dhapi.router.version_checker import suggest_upgrade


def entrypoint():
    sys.tracebacklimit = 0

    suggest_upgrade()

    arg_parser = ArgParser()

    if arg_parser.is_buylotto645():
        ctrl = Lotto645Controller(arg_parser.get_user_id(), arg_parser.get_user_pw())
        ctrl.buy(arg_parser.create_lotto645_req(), arg_parser.is_quiet())
    else:
        raise NotImplementedError("Not implemented yet")
