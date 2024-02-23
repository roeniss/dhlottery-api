from typing import Optional

from dhapi.domain.email_form import EmailForm
from dhapi.domain.user import User
from dhapi.endpoint.lottery_email_sender import LotteryEmailSender
from dhapi.endpoint.lottery_stdout_printer import LotteryStdoutPrinter
from dhapi.endpoint.version_stdout_printer import VersionStdoutPrinter
from dhapi.meta.version_provider import VersionProvider
from dhapi.port.lottery_client import LotteryClient
from dhapi.port.mailjet_email_client import MailjetEmailClient
from dhapi.purchase.lotto645_buy_confirmer import Lotto645BuyConfirmer


def build_lottery_client(user_profile: User, email_form: Optional[EmailForm]):
    lottery_endpoint = build_lottery_endpoint(email_form)
    return LotteryClient(user_profile, lottery_endpoint)


def build_lotto645_buy_confirmer():
    return Lotto645BuyConfirmer()


def build_email_client(api_key, api_secret):
    return MailjetEmailClient(api_key, api_secret)


def build_lottery_endpoint(email_form: EmailForm):
    if email_form:
        email_client = build_email_client(email_form.api_key, email_form.api_secret)
        return LotteryEmailSender(email_client, email_form.sender_email, email_form.recipient_email)
    else:
        return LotteryStdoutPrinter()


def build_version_provider():
    version_endpoint = build_version_endpoint()
    return VersionProvider(version_endpoint)


def build_version_endpoint():
    return VersionStdoutPrinter()
