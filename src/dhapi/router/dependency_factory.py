from dhapi.domain.user import User
from dhapi.endpoint.lottery_stdout_printer import LotteryStdoutPrinter
from dhapi.endpoint.version_stdout_printer import VersionStdoutPrinter
from dhapi.meta.version_provider import VersionProvider
from dhapi.port.lottery_client import LotteryClient
from dhapi.purchase.lotto645_buy_confirmer import Lotto645BuyConfirmer


def build_lottery_client(user_profile: User):
    lottery_endpoint = build_lottery_endpoint()
    return LotteryClient(user_profile, lottery_endpoint)


def build_lotto645_buy_confirmer():
    return Lotto645BuyConfirmer()


def build_lottery_endpoint():
    return LotteryStdoutPrinter()


def build_version_provider():
    version_endpoint = build_version_endpoint()
    return VersionProvider(version_endpoint)


def build_version_endpoint():
    return VersionStdoutPrinter()
