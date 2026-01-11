import datetime
import json
import logging
import re
import time
from typing import List, Dict

import pytz
import requests
from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from dhapi.domain.deposit import Deposit
from dhapi.domain.lotto645_ticket import Lotto645Ticket, Lotto645Mode
from dhapi.domain.user import User

logger = logging.getLogger(__name__)


class LotteryClient:
    _base_url = "https://www.dhlottery.co.kr"
    _login_page = "/login"
    _rsa_key_url = "/login/selectRsaModulus.do"
    _login_url = "/login/securityLoginCheck.do"
    _buy_lotto645_url = "https://ol.dhlottery.co.kr/olotto/game/execBuy.do"
    _ready_socket = "https://ol.dhlottery.co.kr/olotto/game/egovUserReadySocket.json"
    _game645_page = "https://ol.dhlottery.co.kr/olotto/game/game645.do"
    _cash_balance = "https://www.dhlottery.co.kr/mypage/home"
    _assign_virtual_account_1 = "https://www.dhlottery.co.kr/kbank.do?method=kbankInit"
    _assign_virtual_account_2 = "https://www.dhlottery.co.kr/kbank.do?method=kbankProcess"
    _lotto_buy_list_url = "https://www.dhlottery.co.kr/mypage/selectMyLotteryledger.do"
    _DETAIL_REQUEST_DELAY = 0.5

    def __init__(self, user_profile: User, lottery_endpoint):
        self._user_id = user_profile.username
        self._user_pw = user_profile.password
        self._lottery_endpoint = lottery_endpoint

        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
            }
        )

        self._login()

    def _rsa_encrypt(self, plain_text, modulus_hex, exponent_hex):
        n = int(modulus_hex, 16)
        e = int(exponent_hex, 16)
        key = RSA.construct((n, e))
        cipher = PKCS1_v1_5.new(key)
        encrypted = cipher.encrypt(plain_text.encode("utf-8"))
        return encrypted.hex()

    def _login(self):
        resp = self._session.get(f"{self._base_url}/", timeout=10)
        logger.debug(f"Initial session status: {resp.status_code}")

        if "index_check.html" in resp.url:
            raise RuntimeError("동행복권 사이트가 현재 시스템 점검중입니다.")

        resp = self._session.get(f"{self._base_url}{self._login_page}", timeout=10)
        logger.debug(f"Login page status: {resp.status_code}")

        # RSA 공개키 요청
        rsa_headers = {"Accept": "application/json", "X-Requested-With": "XMLHttpRequest", "Referer": f"{self._base_url}{self._login_page}"}
        resp = self._session.get(f"{self._base_url}{self._rsa_key_url}", headers=rsa_headers, timeout=10)
        rsa_data = resp.json()

        if "data" not in rsa_data:
            raise RuntimeError("RSA 키를 가져올 수 없습니다.")

        rsa_modulus = rsa_data["data"]["rsaModulus"]
        rsa_exponent = rsa_data["data"]["publicExponent"]
        logger.debug(f"RSA key received, modulus length: {len(rsa_modulus)}")

        # 아이디/비밀번호 암호화 및 로그인
        encrypted_user_id = self._rsa_encrypt(self._user_id, rsa_modulus, rsa_exponent)
        encrypted_password = self._rsa_encrypt(self._user_pw, rsa_modulus, rsa_exponent)

        login_headers = {"Content-Type": "application/x-www-form-urlencoded", "Origin": self._base_url, "Referer": f"{self._base_url}{self._login_page}"}
        login_data = {"userId": encrypted_user_id, "userPswdEncn": encrypted_password, "inpUserId": self._user_id}

        resp = self._session.post(f"{self._base_url}{self._login_url}", headers=login_headers, data=login_data, timeout=10, allow_redirects=True)
        logger.debug(f"Login response status: {resp.status_code}, URL: {resp.url}")

        if resp.status_code != 200 or "loginSuccess" not in resp.url:
            soup = BeautifulSoup(resp.text, "html5lib")
            error_button = soup.find("a", {"class": "btn_common"})
            if error_button:
                raise RuntimeError("로그인에 실패했습니다. 아이디 또는 비밀번호를 확인해주세요.")
            raise RuntimeError(f"로그인에 실패했습니다. (Status: {resp.status_code}, URL: {resp.url})")

        logger.debug("로그인 성공")

        # 구매 도메인(ol.dhlottery.co.kr)에 접속하여 JSESSIONID 획득
        resp = self._session.get(f"{self._base_url}/main", timeout=10)
        logger.debug(f"Main page status: {resp.status_code}")

        resp = self._session.get(self._game645_page, timeout=10, allow_redirects=True)
        logger.debug(f"ol.dhlottery.co.kr visit status: {resp.status_code}")

        for cookie in self._session.cookies:
            logger.debug(f"Cookie: {cookie.name} = {cookie.value[:20]}... (domain: {cookie.domain})")

        if not any(c.name == "JSESSIONID" for c in self._session.cookies):
            logger.warning("JSESSIONID was not acquired from ol.dhlottery.co.kr")

    def _get_round(self):
        """
        로또645 현재 판매 중인 회차를 계산

        로또645는 2002년 12월 7일(토요일)부터 매주 토요일마다 추첨.
        1회부터 현재까지 경과한 주 수를 계산하여 회차를 반환.

        Returns:
            int: 현재 판매 중인 회차 번호
        """
        first_round_date = datetime.date(2002, 12, 7)
        korea_tz = pytz.timezone("Asia/Seoul")
        now = datetime.datetime.now(korea_tz)
        today = now.date()

        current_weekday = today.weekday()
        days_until_saturday = (5 - current_weekday) % 7
        this_saturday = today + datetime.timedelta(days=days_until_saturday)

        days_diff = (this_saturday - first_round_date).days
        weeks_passed = days_diff // 7
        round_number = 1 + weeks_passed

        logger.debug(f"Calculated round: {round_number} (today: {today}, this_saturday: {this_saturday})")
        return round_number

    def _calculate_draw_dates(self):
        korea_tz = pytz.timezone("Asia/Seoul")
        now = datetime.datetime.now(korea_tz)
        today = now.date()
        current_weekday = today.weekday()
        days_until_saturday = (5 - current_weekday) % 7
        draw_date = today + datetime.timedelta(days=days_until_saturday)
        pay_limit_date = draw_date + datetime.timedelta(days=365)
        return draw_date, pay_limit_date

    def buy_lotto645(self, tickets: List[Lotto645Ticket]):
        try:
            res = self._session.post(url=self._ready_socket, timeout=5)
            direct = json.loads(res.text)["ready_ip"]

            round_number = self._get_round()
            draw_date, pay_limit_date = self._calculate_draw_dates()

            data = {
                "round": str(round_number),
                "direct": direct,
                "nBuyAmount": str(1000 * len(tickets)),
                "param": self._make_buy_loyyo645_param(tickets),
                "ROUND_DRAW_DATE": draw_date.strftime("%Y/%m/%d"),
                "WAMT_PAY_TLMT_END_DT": pay_limit_date.strftime("%Y/%m/%d"),
                "gameCnt": len(tickets),
                "saleMdaDcd": "10",
            }
            logger.debug(f"data: {data}")

            buy_headers = {"Referer": self._game645_page, "Origin": "https://ol.dhlottery.co.kr"}

            resp = self._session.post(self._buy_lotto645_url, headers=buy_headers, data=data, timeout=10)

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
            resp = self._session.get(self._cash_balance, timeout=10)
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

            params = {
                "srchStrDt": start_dt.strftime("%Y%m%d"),
                "srchEndDt": end_dt.strftime("%Y%m%d"),
                "sort": "",
                "ltGdsCd": "",
                "winResult": "",
                "pageNum": 1,
                "recordCountPerPage": 100,
                "_": int(datetime.datetime.now().timestamp() * 1000),
            }

            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.dhlottery.co.kr/mypage/mylotteryledger",
            }

            self._session.get("https://www.dhlottery.co.kr/mypage/mylotteryledger", timeout=10)

            resp = self._session.get(self._lotto_buy_list_url, params=params, headers=headers, timeout=10)

            if resp.status_code != 200:
                logger.error(f"API 요청 실패: {resp.status_code}")
                raise RuntimeError(f"구매 내역 조회 API 요청 실패 (Status: {resp.status_code})")

            content_type = resp.headers.get("Content-Type", "")
            if "application/json" not in content_type:
                logger.error(f"JSON이 아닌 응답: {content_type}, URL: {resp.url}")
                raise RuntimeError("구매 내역 조회 API가 JSON을 반환하지 않았습니다. 세션이 만료되었을 수 있습니다.")

            data = resp.json()

            found_data = self._parse_buy_list_json(data)

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

    def _parse_buy_list_json(self, response_data):
        if not response_data or "data" not in response_data:
            return []

        data = response_data.get("data", {})
        items = data.get("list", [])

        if not items:
            return []

        headers = ["구입일자", "복권명", "회차", "선택번호/복권번호", "구입매수", "당첨결과", "당첨금", "추첨일"]
        rows = []

        for item in items:
            purchase_date = item.get("eltOrdrDt", "")
            lottery_name = item.get("ltGdsNm", "")
            round_no = item.get("ltEpsdView", "")
            gm_info = item.get("gmInfo", "")
            quantity = str(item.get("prchsQty", ""))
            win_result = item.get("ltWnResult", "")
            ntsl_ordr_no = item.get("ntslOrdrNo", "")
            win_amt = item.get("ltWnAmt", 0)
            draw_date = item.get("epsdRflDt", "")

            win_amt_str = f"{win_amt:,}원" if win_amt > 0 else "-"

            if gm_info and lottery_name in ["로또645", "로또6/45"] and ntsl_ordr_no:
                numbers = self._get_lotto645_ticket_detail(ntsl_ordr_no, gm_info, purchase_date)
                time.sleep(self._DETAIL_REQUEST_DELAY)
            else:
                numbers = gm_info

            if lottery_name in ["로또645", "로또6/45"]:
                lottery_name = "로또6/45"

            rows.append([purchase_date, lottery_name, round_no, numbers, quantity, win_result, win_amt_str, draw_date])

        return [{"headers": headers, "rows": rows}]

    def _get_lotto645_ticket_detail(self, ntsl_ordr_no, barcode, purchase_date):
        """로또645 티켓 상세 정보 조회

        Args:
            ntsl_ordr_no: 주문번호
            barcode: 바코드 (gmInfo)
            purchase_date: 구매일 (YYYY-MM-DD)

        Returns:
            str: 포맷팅된 번호 정보
        """
        try:
            import datetime

            purchase_dt = datetime.datetime.strptime(purchase_date, "%Y-%m-%d").date()
            start_date = (purchase_dt - datetime.timedelta(days=7)).strftime("%Y%m%d")
            end_date = (purchase_dt + datetime.timedelta(days=7)).strftime("%Y%m%d")

            url = "https://www.dhlottery.co.kr/mypage/lotto645TicketDetail.do"
            params = {"ntslOrdrNo": ntsl_ordr_no, "srchStrDt": start_date, "srchEndDt": end_date, "barcd": barcode}

            resp = self._session.get(url, params=params, timeout=10)
            data = resp.json()

            if not data.get("data", {}).get("success"):
                return "조회 실패"

            ticket = data["data"]["ticket"]
            game_dtl = ticket.get("game_dtl", [])

            if not game_dtl:
                return "번호 정보 없음"

            type_map = {1: "수동", 2: "반자동", 3: "자동"}

            result = []
            for game in game_dtl:
                idx = game.get("idx", "")
                numbers = game.get("num", [])
                game_type = type_map.get(game.get("type", 3), "자동")

                if numbers:
                    numbers_str = " ".join(str(n) for n in numbers)
                    result.append(f"[{idx}] {game_type}: {numbers_str}")

            return "\n".join(result) if result else "번호 확인 불가"

        except Exception as e:
            logger.error(f"로또 상세 정보 조회 실패: {e}")
            return "조회 실패"

    def _parse_digit(self, text):
        return int("".join(filter(str.isdigit, text)))

    def assign_virtual_account(self, deposit: Deposit):
        try:
            resp = self._session.post(
                self._assign_virtual_account_1,
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

            resp = self._session.post(self._assign_virtual_account_2, data=body, timeout=10)
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
