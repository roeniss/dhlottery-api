from dhapi.purchase.lotto645_controller import Lotto645Controller
from dhapi.router.arg_parser import ArgParser
from dhapi.configuration.logger import set_logger


def entrypoint():
    arg_parser = ArgParser()

    set_logger(arg_parser.get_is_debug())

    if arg_parser.is_buylotto645():
        ctrl = Lotto645Controller(arg_parser.get_user_id(), arg_parser.get_user_pw())
        ctrl.buy(arg_parser.create_lotto645_req(), arg_parser.is_quiet())
    else:
        raise NotImplementedError("Not implemented yet")
