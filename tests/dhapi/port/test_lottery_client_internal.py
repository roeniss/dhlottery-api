import json
import pytest

from dhapi.domain.lotto645_ticket import Lotto645Ticket, Lotto645Mode
from dhapi.port.lottery_client import LotteryClient


def _make_client():
    return object.__new__(LotteryClient)


def test_format_lotto_numbers():
    client = _make_client()
    lines = ["A|01|02|03|04|05|063", "B|11|12|13|14|15|261"]
    slots = client._format_lotto_numbers(lines)

    assert slots == [
        {"mode": "자동", "slot": "A", "numbers": ["01", "02", "03", "04", "05", "06"]},
        {"mode": "수동", "slot": "B", "numbers": ["11", "12", "13", "14", "15", "26"]},
    ]


def test_make_buy_loyyo645_param():
    client = _make_client()
    manual = Lotto645Ticket("1,2,3,4,5,6")
    semiauto = Lotto645Ticket("1,2,3")
    auto = Lotto645Ticket()

    params = json.loads(client._make_buy_loyyo645_param([manual, semiauto, auto]))
    assert params == [
        {"genType": "1", "arrGameChoiceNum": "1,2,3,4,5,6", "alpabet": "A"},
        {"genType": "2", "arrGameChoiceNum": "1,2,3", "alpabet": "B"},
        {"genType": "0", "arrGameChoiceNum": None, "alpabet": "C"},
    ]
