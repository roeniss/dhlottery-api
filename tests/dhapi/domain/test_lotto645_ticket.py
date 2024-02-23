import pytest

from dhapi.domain.lotto645_ticket import Lotto645Ticket, Lotto645Mode


def test_create_auto_tickets_makes_auto_tickets():
    tickets = Lotto645Ticket.create_auto_tickets(1)

    assert len(tickets) == 1
    _assert_auto_ticket(tickets[0])


@pytest.mark.parametrize("count", [1, 2, 3, 4, 5])
def test_create_auto_tickets_makes_tickets_with_specified_count(count):
    tickets = Lotto645Ticket.create_auto_tickets(count)

    assert len(tickets) == count


@pytest.mark.parametrize("size", [[''], ['', ''], ['', '', ''], ['', '', '', ''], ['', '', '', '', '']])
def test_create_tickets_makes_tickets_with_specified_size(size):
    tickets = Lotto645Ticket.create_tickets(size)

    assert len(tickets) == len(size)


def test_create_tickets_makes_auto_ticket_with_empty_string():
    tickets = Lotto645Ticket.create_tickets([''])

    assert len(tickets) == 1
    _assert_auto_ticket(tickets[0])


def test_create_tickets_makes_auto_ticket_with_none():
    tickets = Lotto645Ticket.create_tickets([None])

    assert len(tickets) == 1
    _assert_auto_ticket(tickets[0])


def test_create_tickets_makes_semiauto_ticket_with_three_numbers():
    tickets = Lotto645Ticket.create_tickets(['1,2,3'])

    assert len(tickets) == 1
    _assert_semiauto_ticket(tickets[0], [1, 2, 3])


def test_create_tickets_makes_manual_ticket_with_six_numbers():
    tickets = Lotto645Ticket.create_tickets(['1,2,3,4,5,6'])

    assert len(tickets) == 1
    _assert_manual_ticket(tickets[0], [1, 2, 3, 4, 5, 6])


def _assert_auto_ticket(ticket):
    assert ticket.mode == Lotto645Mode.AUTO
    assert len(ticket.numbers) == 0


def _assert_semiauto_ticket(ticket, fixed_numbers):
    assert ticket.mode == Lotto645Mode.SEMIAUTO
    assert len(ticket.numbers) == len(fixed_numbers)
    for n in fixed_numbers:
        assert n in ticket.numbers


def _assert_manual_ticket(ticket, fixed_numbers):
    assert ticket.mode == Lotto645Mode.MANUAL
    assert len(ticket.numbers) == 6
    assert len(fixed_numbers) == 6
    for n in fixed_numbers:
        assert n in ticket.numbers


def test_create_tickets_failed_with_nondigit_value():
    numbers = 'a,b,c'

    with pytest.raises(ValueError) as e:
        Lotto645Ticket.create_tickets([numbers])

    assert e.value.args[0] == '숫자를 입력하세요 (입력된 값: a,b,c).'


def test_create_tickets_failed_with_duplicated_numbers():
    numbers = '1,1'

    with pytest.raises(ValueError) as e:
        Lotto645Ticket.create_tickets([numbers])

    assert e.value.args[0] == '중복되지 않도록 숫자들을 입력하세요 (입력된 값: 1,1).'


def test_create_tickets_failed_with_under_range_number():
    numbers = '0'

    with pytest.raises(ValueError) as e:
        Lotto645Ticket.create_tickets([numbers])

    assert e.value.args[0] == '각 번호는 1부터 45까지의 숫자만 사용할 수 있습니다 (입력된 값: 0).'


def test_create_tickets_failed_with_over_range_number():
    numbers = '46'

    with pytest.raises(ValueError) as e:
        Lotto645Ticket.create_tickets([numbers])

    assert e.value.args[0] == '각 번호는 1부터 45까지의 숫자만 사용할 수 있습니다 (입력된 값: 46).'


def test_create_tickets_failed_with_too_many_numbers():
    numbers = '1,2,3,4,5,6,7'

    with pytest.raises(ValueError) as e:
        Lotto645Ticket.create_tickets([numbers])

    assert e.value.args[0] == '숫자는 0개 이상 6개 이하의 숫자를 입력해야 합니다 (입력된 값: 1,2,3,4,5,6,7).'


def test_mode_kor_formatted_return_자동_for_auto():
    tickets = Lotto645Ticket.create_tickets([''])

    assert len(tickets) == 1
    assert tickets[0].mode_kor == "자동"


def test_mode_kor_formatted_return_반자동_for_semiauto():
    tickets = Lotto645Ticket.create_tickets(['1'])

    assert len(tickets) == 1
    assert tickets[0].mode_kor == "반자동"


def test_mode_kor_formatted_return_수동_for_manual():
    tickets = Lotto645Ticket.create_tickets(['1,2,3,4,5,6'])

    assert len(tickets) == 1
    assert tickets[0].mode_kor == "수동"
