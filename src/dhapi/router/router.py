from dhapi.router.arg_parser import ArgParser
from dhapi.router.dependency_factory import build_lotto645_controller


def entrypoint():
    arg_parser = ArgParser()

    if arg_parser.command() == "BUY_LOTTO645":
        ctrl = build_lotto645_controller(arg_parser)
        ctrl.buy(arg_parser.buy_lotto645_req(), arg_parser.is_quiet(), arg_parser.send_result_to_email())
    elif arg_parser.command() == "SHOW_BALANCE":
        ctrl = build_lotto645_controller(arg_parser)
        ctrl.show_balance()
    elif arg_parser.command() == "ASSIGN_VIRTUAL_ACCOUNT":
        ctrl = build_lotto645_controller(arg_parser)
        ctrl.assign_virtual_account(arg_parser.amount())
    else:
        raise NotImplementedError("Not implemented yet")
