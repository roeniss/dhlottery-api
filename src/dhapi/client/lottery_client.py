import json
import logging
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

    def __init__(self):
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            "sec-ch-ua-mobile": "?0",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://dhlottery.co.kr",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "https://dhlottery.co.kr/",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7",
        }
        self._set_default_session()

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

    def login(self, user_id: str, user_pw: str):
        resp = requests.post(
            LotteryClient._login_request_url,
            headers=self._headers,
            data={
                "returnUrl": LotteryClient._main_url,
                "userId": user_id,
                "password": user_pw,
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
        last_drawn_round = int(soup.find("strong", id="lottoDrwNo").text)
        return last_drawn_round + 1

    def buy_lotto645(self, req: Lotto645BuyRequest):
        """
        :param first 첫 번째 복권 게임을 의미한다. 다음 두 가지 형태 중 하나를 가진다.
         - 일반 숫자 5개와 보너스 숫자를 포함하는 list ([1, 2, 3, 4, 5, 6]) (각각 1~45)
         - 자동 또는 반자동을 의미하는 str ("AUTO", "SEMI_AUTO")
         위 내용은 second, third, fourth, fifth 파라미터에도 적용된다.
        """

        resp = requests.post(
            self._buy_lotto645_url,
            headers=self._headers,
            data={
                "round": str(self._get_round()),
                "direct": "172.17.20.52",  # TODO: test if this can be omitted
                "nBuyAmount": str(1000 * req.get_game_count()),
                "param": req.create_dhlottery_request_param(),
                "gameCnt": req.get_game_count(),
                # "ROUND_DRAW_DATE": "2021/06/01", # succeed after commented
                # "WAMT_PAY_TLMT_END_DT": "2022/06/01", # succeed after commented
            },
            timeout=10,
        )

        resp.encoding = "utf-8"

        return json.loads(resp.text)
