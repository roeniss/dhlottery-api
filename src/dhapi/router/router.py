from dhapi.purchase.lotto645_controller import Lotto645Controller
from dhapi.router.arg_parser import ArgParser
from dhapi.configuration.logger import set_logger


def entrypoint():
    arg_parser = ArgParser()

    set_logger(arg_parser.is_debug())

    if arg_parser.command() == "BUY_LOTTO645":
        ctrl = Lotto645Controller(arg_parser.user_id(), arg_parser.user_pw())
        ctrl.buy(arg_parser.buy_lotto645_req(), arg_parser.is_quiet())
    else:
        raise NotImplementedError("Not implemented yet")
