from typing import Dict, List

from rich.console import Console
from rich.table import Table


class LotteryStdoutPrinter:
    def print_result_of_assign_virtual_account(self, 전용가상계좌, 결제신청금액):
        console = Console()

        console.print("✅ 가상계좌를 할당했습니다.")
        console.print("❗️입금 전 계좌주 이름을 꼭 확인하세요.")
        table = Table("전용가상계좌", "결제신청금액")
        table.add_row(전용가상계좌, 결제신청금액)

        console.print(table)

    def print_result_of_show_balance(self, *, 총예치금, 구매가능금액, 예약구매금액, 출금신청중금액, 구매불가능금액, 이번달누적구매금액):
        console = Console()

        console.print("✅ 예치금 현황을 조회했습니다.")
        table = Table("총예치금", "구매가능금액", "예약구매금액", "출금신청중금액", "구매불가능금액", "이번달누적구매금액")
        table.add_row(
            self._num_to_money_str(총예치금),
            self._num_to_money_str(구매가능금액),
            self._num_to_money_str(예약구매금액),
            self._num_to_money_str(출금신청중금액),
            self._num_to_money_str(구매불가능금액),
            self._num_to_money_str(이번달누적구매금액),
        )
        console.print(table)
        console.print("[dim](구매불가능금액 = 예약구매금액 + 출금신청중금액)[/dim]")

    def _num_to_money_str(self, num):
        return f"{num:,} 원"

    def print_result_of_buy_lotto645(self, slots: List[Dict]):
        """
        :param slots: [{"slot": "A", "mode": "자동", "numbers": [1, 2, 3, 4, 5, 6]}, ...]
        :return:
        """
        console = Console()

        console.print("✅ 로또6/45 복권을 구매했습니다.")
        table = Table("슬롯", "Mode", "번호1", "번호2", "번호3", "번호4", "번호5", "번호6")
        for slot in slots:
            table.add_row(slot["slot"], slot["mode"], *slot["numbers"])
        console.print(table)
