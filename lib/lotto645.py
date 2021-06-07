import json

import requests

from . import auth


class Lotto645:
    _lotto645Headers = {
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

    def buyLotto645(self, authController: auth.AuthController, cnt, mode):
        # authController | should.not_be.none
        # cnt | should.be.within(1, 5, msg="list must have 2 items")
        # mode | should.any(should.be.equal("auto"), should.be.equal("manual"))
        self._lotto645Headers["Origin"] = "https://ol.dhlottery.co.kr"
        self._lotto645Headers[
            "Referer"
        ] = "https://ol.dhlottery.co.kr/olotto/game/game645.do"
        self._lotto645Headers["Cookie"] = f"JSESSIONID={authController.jsessionId}"

        data = {
            "round": "967",
            "direct": "172.17.20.52",
            "nBuyAmount": "1000",
            "param": '[{"genType":"0","arrGameChoiceNum":null,"alpabet":"A"},{"genType":"0","arrGameChoiceNum":null,"alpabet":"B"},{"genType":"0","arrGameChoiceNum":null,"alpabet":"C"},{"genType":"0","arrGameChoiceNum":null,"alpabet":"D"},{"genType":"0","arrGameChoiceNum":null,"alpabet":"E"}]',
            "ROUND_DRAW_DATE": "2021/06/12",
            "WAMT_PAY_TLMT_END_DT": "2022/06/13",
            "gameCnt": "5",
        }

        res = requests.post(
            "https://ol.dhlottery.co.kr/olotto/game/execBuy.do",
            headers=self._lotto645Headers,
            data=data,
        )

        res.encoding = "utf-8"
        resp = json.loads(res.text)
        print(resp)
        print(resp["result"]["resultMsg"])
