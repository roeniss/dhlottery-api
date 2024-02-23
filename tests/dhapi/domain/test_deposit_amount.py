import pytest

from dhapi.domain.deposit import Deposit


def test_fail_on_nondigit_amount():
    amount = "a"

    with pytest.raises(ValueError) as e:
        Deposit(amount)

    assert e.value.args[0] == '숫자를 입력하세요 (입력된 값: a).'


def test_fail_on_not_expected_amount():
    amount = 777

    with pytest.raises(ValueError) as e:
        Deposit(amount)

    assert e.value.args[0] == '입금 가능한 금액은 5천원, 1만원, 2만원, 3만원, 5만원, 10만원, 20만원, 30만원, 50만원, 70만원, 100만원입니다 (입력된 값: 777).'


@pytest.mark.parametrize("amount", [5000, 10000, 20000, 30000, 50000, 100000, 200000, 300000, 500000, 700000, 1000000])
def test_success_on_expected_amount(amount):
    deposit = Deposit(amount)

    assert deposit.amount == amount
