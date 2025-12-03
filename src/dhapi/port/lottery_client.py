import datetime
import json
import logging
import re
import time
from typing import List, Dict

import pytz
import requests
from bs4 import BeautifulSoup

from dhapi.domain.deposit import Deposit
from dhapi.domain.lotto645_ticket import Lotto645Ticket, Lotto645Mode
from dhapi.domain.user import User

logger = logging.getLogger(__name__)


class LotteryClient:
    _default_session_url = "https://dhlottery.co.kr/gameResult.do?method=byWin&wiselog=H_C_1_1"
    _system_under_check_url = "https://dhlottery.co.kr/index_check.html"
    _main_url = "https://dhlottery.co.kr/common.do?method=main"
    _login_request_url = "https://www.dhlottery.co.kr/userSsl.do?method=login"
    _buy_lotto645_url = "https://ol.dhlottery.co.kr/olotto/game/execBuy.do"
    _round_info_url = "https://www.dhlottery.co.kr/common.do?method=main"
    _ready_socket = "https://ol.dhlottery.co.kr/olotto/game/egovUserReadySocket.json"
    _cash_balance = "https://dhlottery.co.kr/userSsl.do?method=myPage"
    _assign_virtual_account_1 = "https://dhlottery.co.kr/kbank.do?method=kbankInit"
    _assign_virtual_account_2 = "https://dhlottery.co.kr/kbank.do?method=kbankProcess"
    _lotto_buy_list_url = "https://www.dhlottery.co.kr/myPage.do?method=lottoBuyList"

    def __init__(self, user_profile: User, lottery_endpoint):
        self._user_id = user_profile.username
        self._user_pw = user_profile.password
        self._lottery_endpoint = lottery_endpoint
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            "sec-ch-ua-mobile": "?0",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://dhlottery.co.kr",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "https://dhlottery.co.kr",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7",
            "X-Requested-With": "XMLHttpRequest",
        }
        self._set_default_session()
        self._login()

    # 로그인을 시도하면 새로운 JSESSIONID 값이 내려오는데,
    #  이 값으로 갱신하면 로그인이 풀리는 듯하여 헤더를 갱신하지 않음
    def _set_default_session(self):
        resp = requests.get(LotteryClient._default_session_url, timeout=10)
        logger.debug(f"resp.status_code: {resp.status_code}")
        logger.debug(f"resp.headers: {resp.headers}")

        if resp.url == LotteryClient._system_under_check_url:
            raise RuntimeError("동행복권 사이트가 현재 시스템 점검중입니다.")

        for cookie in resp.cookies:
            if cookie.name == "JSESSIONID":
                self._headers["Cookie"] = f"JSESSIONID={cookie.value}"
                break
        else:
            raise RuntimeError("JSESSIONID 쿠키가 정상적으로 세팅되지 않았습니다.")

    def _login(self):
        resp = requests.post(
            LotteryClient._login_request_url,
            headers=self._headers,
            data={
                "returnUrl": LotteryClient._main_url,
                "userId": self._user_id,
                "password": self._user_pw,
                "checkSave": "off",
                "newsEventYn": "",
            },
            timeout=10,
        )
        soup = BeautifulSoup(resp.text, "html5lib")
        if soup.find("a", {"class": "btn_common"}) is not None:
            raise RuntimeError(
                "로그인에 실패했습니다. 아이디 또는 비밀번호를 확인해주세요. (5회 실패했을 수도 있습니다. 이 경우엔 홈페이지에서 비밀번호를 변경해야 합니다)"
            )  # TODO(roeniss): 명확히 구분해서 알려주기

    def _get_round(self):
        resp = requests.get(self._round_info_url, timeout=10)
        soup = BeautifulSoup(resp.text, "html5lib")  # 'html5lib' : in case that the html don't have clean tag pairs

        elem = soup.find("strong", {"id": "lottoDrwNo"})
        if not elem:
            raise RuntimeError("현재 회차 정보를 가져올 수 없습니다.")

        return int(elem.text) + 1

    def buy_lotto645(self, tickets: List[Lotto645Ticket]):
        try:
            res = requests.post(url=self._ready_socket, headers=self._headers, timeout=5)
            direct = json.loads(res.text)["ready_ip"]

            logger.debug(f"direct: {direct}")

            data = {
                "round": str(self._get_round()),
                "direct": direct,
                "nBuyAmount": str(1000 * len(tickets)),
                "param": self._make_buy_loyyo645_param(tickets),
                "gameCnt": len(tickets),
            }
            logger.debug(f"data: {data}")

            resp = requests.post(
                self._buy_lotto645_url,
                headers=self._headers,
                data=data,
                timeout=10,
            )

            response_text = resp.text
            logger.debug(f"response: {response_text}")

            response = json.loads(response_text)
            if not self._is_purchase_success(response):
                raise RuntimeError(f"❗ 로또6/45 구매에 실패했습니다. (사유: {response['result']['resultMsg']})")

            slots = self._format_lotto_numbers(response["result"]["arrGameChoiceNum"])
            self._lottery_endpoint.print_result_of_buy_lotto645(slots)
        except RuntimeError as e:
            raise e
        except Exception:
            raise RuntimeError("❗ 로또6/45 구매에 실패했습니다. (사유: 알 수 없는 오류)")

    def _is_purchase_success(self, response):
        return response["result"]["resultCode"] == "100"

    def _make_buy_loyyo645_param(self, tickets: List[Lotto645Ticket]):
        params = []
        for i, t in enumerate(tickets):
            if t.mode == Lotto645Mode.AUTO:
                gen_type = "0"
            elif t.mode == Lotto645Mode.MANUAL:
                gen_type = "1"
            elif t.mode == Lotto645Mode.SEMIAUTO:
                gen_type = "2"
            else:
                raise RuntimeError(f"올바르지 않은 모드입니다. (mode: {t.mode})")
            arr_game_choice_num = None if t.mode == Lotto645Mode.AUTO else ",".join(map(str, t.numbers))
            alpabet = "ABCDE"[i]  # XXX: 오타 아님
            slot = {
                "genType": gen_type,
                "arrGameChoiceNum": arr_game_choice_num,
                "alpabet": alpabet,
            }
            params.append(slot)
        return json.dumps(params)

    def _format_lotto_numbers(self, lines: list) -> List[Dict]:
        """
        example: ["A|01|02|04|27|39|443", "B|11|23|25|27|28|452"]
        """

        mode_dict = {
            "1": "수동",
            "2": "반자동",
            "3": "자동",
        }

        slots = []
        for line in lines:
            slot = {
                "mode": mode_dict[line[-1]],
                "slot": line[0],
                "numbers": line[2:-1].split("|"),
            }
            slots.append(slot)
        return slots

    def show_balance(self):
        try:
            resp = requests.get(self._cash_balance, headers=self._headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html5lib")

            has_bank_account = soup.select_one(".tbl_total_account_number_top tbody tr td").contents != []
            elem = soup.select("div.box.money")
            elem = elem[0]

            if has_bank_account is True:
                # 간편충전 계좌번호가 있는 경우
                총예치금 = self._parse_digit(elem.select("p.total_new > strong")[0].contents[0])
                구매가능금액 = self._parse_digit(elem.select("td.ta_right")[3].contents[0])
                예약구매금액 = self._parse_digit(elem.select("td.ta_right")[4].contents[0])
                출금신청중금액 = self._parse_digit(elem.select("td.ta_right")[5].contents[0])
                구매불가능금액 = self._parse_digit(elem.select("td.ta_right")[6].contents[0])  # (예약구매금액 + 출금신청중금액)
                이번달누적구매금액 = self._parse_digit(elem.select("td.ta_right")[7].contents[0])
            else:
                # 간편충전 계좌번호가 없는 경우
                총예치금 = self._parse_digit(elem.select("p.total_new > strong")[0].contents[0])
                구매가능금액 = self._parse_digit(elem.select("td.ta_right")[1].contents[0])
                예약구매금액 = self._parse_digit(elem.select("td.ta_right")[2].contents[0])
                출금신청중금액 = self._parse_digit(elem.select("td.ta_right")[3].contents[0])
                구매불가능금액 = self._parse_digit(elem.select("td.ta_right")[4].contents[0])  # (예약구매금액 + 출금신청중금액)
                이번달누적구매금액 = self._parse_digit(elem.select("td.ta_right")[5].contents[0])

            self._lottery_endpoint.print_result_of_show_balance(
                총예치금=총예치금,
                구매가능금액=구매가능금액,
                예약구매금액=예약구매금액,
                출금신청중금액=출금신청중금액,
                구매불가능금액=구매불가능금액,
                이번달누적구매금액=이번달누적구매금액,
            )

        except Exception:
            raise RuntimeError("❗ 예치금 현황을 조회하지 못했습니다.")

    def show_buy_list(self, output_format="table", start_date=None, end_date=None):
        try:
            start_dt, end_dt = self._calculate_date_range(start_date, end_date)

            data = {
                "nowPage": 1,
                "searchStartDate": start_dt.strftime("%Y%m%d"),
                "searchEndDate": end_dt.strftime("%Y%m%d"),
                "lottoId": "",
                "winGrade": 2,
                "calendarStartDt": start_dt.strftime("%Y-%m-%d"),
                "calendarEndDt": end_dt.strftime("%Y-%m-%d"),
                "sortOrder": "DESC",
            }

            resp = requests.post(self._lotto_buy_list_url, headers=self._headers, data=data, timeout=10)
            soup = BeautifulSoup(resp.text, "html5lib")

            tables = soup.find_all("table")
            found_data = self._parse_buy_list_tables(tables)

            self._lottery_endpoint.print_result_of_show_buy_list(found_data, output_format, start_dt.strftime("%Y-%m-%d"), end_dt.strftime("%Y-%m-%d"))

        except Exception as e:
            logger.error(e)
            raise RuntimeError("❗ 구매 내역을 조회하지 못했습니다.")

    def _calculate_date_range(self, start_date, end_date):
        today = datetime.date.today()

        if start_date:
            start_dt = datetime.datetime.strptime(start_date, "%Y%m%d").date()
        else:
            start_dt = today - datetime.timedelta(days=14)

        if end_date:
            end_dt = datetime.datetime.strptime(end_date, "%Y%m%d").date()
        else:
            end_dt = today
        return start_dt, end_dt

    def _parse_buy_list_tables(self, tables):
        found_data = []
        for table in tables:
            headers = [th.text.strip() for th in table.find_all("th")]
            rows = []
            for tr in table.find_all("tr"):
                cols = []
                detail_info = None
                tds = tr.find_all("td")
                for i, td in enumerate(tds):
                    text = td.text.strip()
                    cols.append(text)

                    if i == 3:
                        detail_info = self._extract_detail_info(td)

                if cols:
                    if detail_info:
                        numbers = self._get_lotto645_detail(detail_info)
                        time.sleep(0.5)  # 500ms sleep for dhlottery server
                        cols[3] = numbers
                    rows.append(cols)

            if rows:
                found_data.append({"headers": headers, "rows": rows})
        return found_data

    def _extract_detail_info(self, td):
        link = td.find("a")
        if link and "javascript:detailPop" in link.get("href", ""):
            href = link.get("href")
            match = re.search(r"detailPop\('([^']*)',\s*'([^']*)',\s*'([^']*)'\)", href)
            if match:
                return {
                    "orderNo": match.group(1),
                    "barcode": match.group(2),
                    "issueNo": match.group(3),
                }
        return None

    def _get_lotto645_detail(self, detail_info):
        try:
            url = (
                f"https://www.dhlottery.co.kr/myPage.do?method=lotto645Detail"
                f"&orderNo={detail_info['orderNo']}"
                f"&barcode={detail_info['barcode']}"
                f"&issueNo={detail_info['issueNo']}"
            )
            resp = requests.get(url, headers=self._headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html5lib")

            result = []
            selected_div = soup.find("div", {"class": "selected"})
            if selected_div:
                for li in selected_div.find_all("li"):
                    strong = li.find("strong")
                    if not strong:
                        continue
                    spans = strong.find_all("span")
                    if len(spans) < 2:
                        continue

                    slot = spans[0].text.strip()
                    mode = " ".join(spans[1].text.split())

                    nums_div = li.find("div", {"class": "nums"})
                    if nums_div:
                        numbers = self._extract_leaf_numbers(nums_div)
                        if numbers:
                            result.append(f"[{slot}] {mode}: {' '.join(numbers)}")

            if result:
                return "\n".join(result)

            return "번호 확인 불가"

        except Exception as e:
            logger.error(f"로또 상세 정보 조회 실패: {e}")
            return "조회 실패"

    def _extract_leaf_numbers(self, nums_div):
        numbers = []
        for span in nums_div.find_all("span"):
            if not span.find("span"):
                text = span.text.strip()
                if text.isdigit():
                    numbers.append(text)
        return numbers

    def _parse_digit(self, text):
        return int("".join(filter(str.isdigit, text)))

    def assign_virtual_account(self, deposit: Deposit):
        try:
            resp = requests.post(
                self._assign_virtual_account_1,
                headers=self._headers,
                data={
                    "PayMethod": "VBANK",
                    "VbankBankCode": "089",  # 가상계좌 채번가능 케이뱅크 코드
                    "price": str(deposit.amount),
                    "goodsName": "복권예치금",
                    "vExp": self._get_tomorrow(),
                },
                timeout=10,
            )
            logger.debug(f"status_code: {resp.status_code}")

            data = resp.json()
            logger.debug(f"data: {data}")

            body = {
                "PayMethod": "VBANK",
                "GoodsName": data["GoodsName"],
                "GoodsCnt": "",
                "BuyerTel": data["BuyerTel"],
                "Moid": data["Moid"],
                "MID": data["MID"],
                "UserIP": data["UserIP"],
                "MallIP": data["MallIP"],
                "MallUserID": data["MallUserID"],
                "VbankExpDate": data["VbankExpDate"],
                "BuyerEmail": data["BuyerEmail"],
                # "SocketYN": '',
                # "GoodsCl": '',
                # "EncodeParameters": '',
                "EdiDate": data["EdiDate"],
                "EncryptData": data["EncryptData"],
                "Amt": data["amt"],
                "BuyerName": data["BuyerName"],
                "VbankBankCode": data["VbankBankCode"],
                "VbankNum": data["FxVrAccountNo"],
                "FxVrAccountNo": data["FxVrAccountNo"],
                "VBankAccountName": data["BuyerName"],
                "svcInfoPgMsgYn": "N",
                "OptionList": "no_receipt",
                "TransType": "0",  # 일반(0), 에스크로(1)
                # "TrKey": None,
            }
            logger.debug(f"body: {body}")

            resp = requests.post(self._assign_virtual_account_2, headers=self._headers, data=body, timeout=10)
            logger.debug(f"resp: {resp}")
            logger.debug(f"resp.text: {resp.text}")

            soup = BeautifulSoup(resp.text, "html5lib")

            elem = soup.select("#contents")

            logger.debug(f"elem: {elem}")

            전용가상계좌 = elem[0].select("span")[0].contents[0]
            결제신청금액 = elem[0].select(".color_key1")[0].contents[0]

            self._lottery_endpoint.print_result_of_assign_virtual_account(전용가상계좌, 결제신청금액)
        except Exception:
            raise RuntimeError("❗ 가상계좌를 할당하지 못했습니다.")

    def _get_tomorrow(self):
        korea_tz = pytz.timezone("Asia/Seoul")
        now = datetime.datetime.now(korea_tz)
        tomorrow = now + datetime.timedelta(days=1)
        return tomorrow.strftime("%Y%m%d")
