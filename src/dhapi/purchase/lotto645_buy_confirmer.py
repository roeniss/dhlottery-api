import logging
from typing import List

from rich.console import Console
from rich.table import Table

from dhapi.domain.lotto645_ticket import Lotto645Ticket

logger = logging.getLogger(__name__)


class Lotto645BuyConfirmer:
    def confirm(self, tickets: List[Lotto645Ticket], always_yes: bool = False):
        self._show_buy_preview(tickets)
        print("❓ 위와 같이 구매하시겠습니까? [Y/n] ", end="")

        if always_yes:
            print("\n✅ --yes 플래그가 주어져 자동으로 구매를 진행합니다.")
            return True
        elif input().strip().lower() in ["y", "yes", ""]:
            return True

        print("❗️구매를 취소했습니다.")
        return False

    def _show_buy_preview(self, tickets):
        slots = "ABCDE"

        console = Console()
        table = Table("슬롯", "Mode", "번호1", "번호2", "번호3", "번호4", "번호5", "번호6")
        for i, ticket in enumerate(tickets):
            table.add_row(slots[i], ticket.mode_kor, *self._numbers_formatted(ticket.numbers))

        console.print(table)

    def _numbers_formatted(self, numbers: List[int]):
        _numbers = numbers[::]
        _numbers = [str(n) for n in _numbers]
        for _ in range(6 - len(_numbers)):
            _numbers.append("-")
        return _numbers
