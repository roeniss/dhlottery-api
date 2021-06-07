import copy

import requests


class AuthController:
    _authHeaders = {
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

    def __init__(self):
        self.__JSESSIONID = self._getJSESSIONID()

    @property
    def jsessionId(self):  # getter
        return self.__JSESSIONID

    def _getJSESSIONID(self):
        res = requests.get(
            "https://dhlottery.co.kr/gameResult.do?method=byWin&wiselog=H_C_1_1"
        )
        for cookie in res.cookies:
            if cookie.name == "JSESSIONID":
                return cookie.value
        raise Exception("Fail to get JSESSIONID")

    def login(self, userId, password):
        self._authHeaders["Cookie"] = f"JSESSIONID={self.__JSESSIONID}"

        data = {
            "returnUrl": "https://dhlottery.co.kr/common.do?method=main",
            "userId": userId,
            "password": password,
            "checkSave": "on",
        }

        res = requests.post(
            "https://www.dhlottery.co.kr/userSsl.do?method=login",
            headers=self._authHeaders,
            data=data,
        )

        return res
