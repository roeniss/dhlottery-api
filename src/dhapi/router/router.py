from dhapi.client.lottery_client import LotteryClient
from dhapi.client.mailjet_email_client import MailjetEmailClient
from dhapi.purchase.lotto645_controller import Lotto645Controller
from dhapi.router.arg_parser import ArgParser


def entrypoint():
    arg_parser = ArgParser()

    if arg_parser.command() == "BUY_LOTTO645":
        lottery_client = LotteryClient(arg_parser.user_id(), arg_parser.user_pw())
        email_client = MailjetEmailClient(arg_parser.email(), arg_parser.mailjet_api_key(), arg_parser.mailjet_api_secret(), arg_parser.mailjet_sender_email())
        ctrl = Lotto645Controller(lottery_client, email_client)
        ctrl.buy(arg_parser.buy_lotto645_req(), arg_parser.is_quiet(), arg_parser.send_result_to_email())
    else:
        raise NotImplementedError("Not implemented yet")
