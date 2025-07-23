from dhapi.domain.lotto645_ticket import Lotto645Ticket
from dhapi.purchase.lotto645_buy_confirmer import Lotto645BuyConfirmer


def test_numbers_formatted_adds_dashes():
    confirmer = Lotto645BuyConfirmer()
    assert confirmer._numbers_formatted([1, 2, 3]) == ["1", "2", "3", "-", "-", "-"]


def test_confirm_returns_true_when_always_yes():
    confirmer = Lotto645BuyConfirmer()
    confirmer._show_buy_preview = lambda tickets: None
    result = confirmer.confirm([Lotto645Ticket()], always_yes=True)
    assert result is True
