import datetime
import json
import logging
import traceback

import pytz
import requests
from bs4 import BeautifulSoup

from dhapi.domain_object.lotto645_buy_request import Lotto645BuyRequest

logger = logging.getLogger(__name__)


# TODO : LotteryClient 를 한번만 만들어 쓰도록 Singleton/DI 적용
class LotteryClient:
    _default_session_url = "https://dhlottery.co.kr/gameResult.do?method=byWin&wiselog=H_C_1_1"
    _system_under_check_url = "https://dhlottery.co.kr/index_check.html"
    _main_url = "https://dhlottery.co.kr/common.do?method=main"
    _login_request_url = "https://www.dhlottery.co.kr/userSsl.do?method=login"
    _buy_lotto645_url = "https://ol.dhlottery.co.kr/olotto/game/execBuy.do"
    _round_info_url = "https://www.dhlottery.co.kr/common.do?method=main"
    _ready_socket = "https://ol.dhlottery.co.kr/olotto/game/egovUserReadySocket.json"
    _cash_balance = "https://dhlottery.co.kr/userSsl.do?method=myPage"
    _assign_virtual_account_1 = "https://dhlottery.co.kr/nicePay.do?method=nicePayInit"
    _assign_virtual_account_2 = "https://dhlottery.co.kr/nicePay.do?method=nicePayProcess"

    def __init__(self, user_id: str, user_pw: str):
        self._user_id = user_id
        self._user_pw = user_pw
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
        self.login()

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

    def login(self):
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
            raise RuntimeError("로그인에 실패했습니다. 아이디 또는 비밀번호를 확인해주세요.")

    def _get_round(self):
        resp = requests.get(self._round_info_url, timeout=10)
        soup = BeautifulSoup(resp.text, "html5lib")  # 'html5lib' : in case that the html don't have clean tag pairs

        elem = soup.find("strong", {"id": "lottoDrwNo"})
        if not elem:
            raise RuntimeError("현재 회차 정보를 가져올 수 없습니다.")

        return int(elem.text) + 1

    def buy_lotto645(self, req: Lotto645BuyRequest):
        """
        :param first 첫 번째 복권 게임을 의미한다. 다음 두 가지 형태 중 하나를 가진다.
         - 일반 숫자 5개와 보너스 숫자를 포함하는 list ([1, 2, 3, 4, 5, 6]) (각각 1~45)
         - 자동 또는 반자동을 의미하는 str ("AUTO", "SEMI_AUTO")
         위 내용은 second, third, fourth, fifth 파라미터에도 적용된다.
        """

        res = requests.post(url=self._ready_socket, headers=self._headers, timeout=5)
        direct = json.loads(res.text)["ready_ip"]

        logger.debug(f"direct: {direct}")

        data = {
            "round": str(self._get_round()),
            "direct": direct,
            "nBuyAmount": str(1000 * req.get_game_count()),
            "param": req.create_dhlottery_request_param(),
            "gameCnt": req.get_game_count(),
        }
        logger.debug(f"data: {data}")
        resp = requests.post(
            self._buy_lotto645_url,
            headers=self._headers,
            data=data,
            timeout=10,
        )

        logger.debug(f"resp.text: {resp.text}")

        return json.loads(resp.text)

    def get_balance(self):
        resp = requests.get(self._cash_balance, headers=self._headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html5lib")

        elem = soup.select("div.box.money")
        try:
            elem = elem[0]

            총예치금 = self._parse_digit(elem.select("p.total_new > strong")[0].contents[0])
            구매가능금액 = self._parse_digit(elem.select("td.ta_right")[3].contents[0])
            예약구매금액 = self._parse_digit(elem.select("td.ta_right")[4].contents[0])
            출금신청중금액 = self._parse_digit(elem.select("td.ta_right")[5].contents[0])
            구매불가능금액 = self._parse_digit(elem.select("td.ta_right")[6].contents[0])  # (예약구매금액 + 출금신청중금액)
            이번달누적구매금액 = self._parse_digit(elem.select("td.ta_right")[7].contents[0])

            return {
                "총예치금": 총예치금,
                "구매가능금액": 구매가능금액,
                "예약구매금액": 예약구매금액,
                "출금신청중금액": 출금신청중금액,
                "구매불가능금액": 구매불가능금액,
                "이번달누적구매금액": 이번달누적구매금액,
            }
        except IndexError:
            logger.debug(traceback.format_exc())
            logger.error("❗ 잔액 정보를 가져오지 못했습니다.")
            return {}

    def _parse_digit(self, text):
        return int("".join(filter(str.isdigit, text)))

    def assign_virtual_account(self, amount):
        if amount not in [5000, 10000, 20000, 30000, 50000, 100000, 200000, 300000, 500000, 700000, 1000000]:
            raise RuntimeError("충전 가능한 금액 단위가 아닙니다. 5000, 10000, 20000, 30000, 50000, 100000, 200000, 300000, 500000, 700000, 1000000 원 중 하나를 입력해주세요.")

        resp = requests.post(self._assign_virtual_account_1,
                             headers=self._headers,
                             data={
                                 "PayMethod": "VBANKFVB01",
                                 "VbankBankCode": "089",  # 가상계좌 채번가능 케이뱅크 코드
                                 "price": str(amount),
                                 "goodsName": "복권예치금",
                                 "vExp": self._get_tomorrow()
                             },
                             timeout=10)
        logger.debug(f"status_code: {resp.status_code}")

        data = resp.json()
        logger.debug(f"data: {data}")

        body = {
            "PayMethod": data["PayMethod"],
            "GoodsName": data["GoodsName"],
            "GoodsCnt": data["GoodsCnt"],
            "BuyerTel": data["BuyerTel"],
            "Moid": data["Moid"],
            "MID": data["MID"],
            "UserIP": data["UserIP"],
            "MallIP": data["MallIP"],
            "MallUserID": data["MallUserID"],
            "VbankExpDate": data["VbankExpDate"],
            "BuyerEmail": data["BuyerEmail"],
            "SocketYN": data["SocketYN"],
            "GoodsCl": data["GoodsCl"],
            "EncodeParameters": data["EncodeParameters"],
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
            "TrKey": None,
        }
        logger.debug(f"body: {body}")

        resp = requests.post(self._assign_virtual_account_2, headers=self._headers, data=body, timeout=10)
        logger.debug(f"resp: {resp}")

        soup = BeautifulSoup(resp.text, "html5lib")

        elem = soup.select("#contents")

        고정가상계좌 = elem[0].select("span")[0].contents[0]
        결제금액 = elem[0].select(".color_key1")[0].contents[0]

        return {
            "고정가상계좌": 고정가상계좌,
            "결제금액": 결제금액,
        }

    def _get_tomorrow(self):
        korea_tz = pytz.timezone('Asia/Seoul')
        now = datetime.datetime.now(korea_tz)
        tomorrow = now + datetime.timedelta(days=1)
        return tomorrow.strftime("%Y%m%d")
