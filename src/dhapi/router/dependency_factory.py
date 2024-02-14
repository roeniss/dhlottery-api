from dhapi.client.lottery_client import LotteryClient
from dhapi.client.mailjet_email_client import MailjetEmailClient
from dhapi.purchase.lotto645_controller import Lotto645Controller


def build_lotto645_controller(arg_parser):
    return Lotto645Controller(
        build_lottery_client(arg_parser),
        build_email_client(arg_parser),
    )


def build_lottery_client(arg_parser):
    return LotteryClient(**arg_parser.user_source())


def build_email_client(arg_parser):
    return MailjetEmailClient(**arg_parser.email_source())
