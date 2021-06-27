# DongHaeng Lottery API (Unofficial)

[동행복권](https://dhlottery.co.kr/) 사이트를 터미널에서 이용할 수 있게 랩핑한 API입니다.

현재 제게 필요한 기능이 [로또 6/45](https://dhlottery.co.kr/gameInfo.do?method=gameMethod&wiselog=H_B_1_1) 구매 뿐이라서 해당 부분만 구현되어 있습니다. 만약 다른 기능이 필요하시면 아래 가이드를 따라서 직접 개발하시거나, Github Issues 를 통해 개발 요청을 등록해주시길 바랍니다.

## 사용법

### 설치

// TODO

### 커맨드

현재는 `로또6/45`를 `자동`으로 사는 기능뿐입니다. 갯수(`-c`)는 1에서 5사이로 조절할 수 있습니다. 한 주에 5장 이상을 사려고 하면 구매가 되지 않고 적절한 에러 메시지가 출력됩니다.

헷갈리실까봐 사족을 붙이자면, `auto`는 번호를 자동으로 선택하는 그 자동모드를 말하는 것입니다.

```sh
dhapi -h # Help

dhapi -u YOUR_ID -p YOUR_PW -C lotto645 -t buy -c 5 -m auto # 로또6/45를 - 산다 - 5장 - 자동발급으로
```

## 작동 방식

동행복권 사이트는 `JSESSIONID`를 이용하여 유저를 인증합니다. 본 API에서는 `requests`를 이용해 로그인한 후 `JSESSIONID`를 메모리에 저장해 복권 구매에 활용합니다.

## 개발 가이드

### 개발 환경 세팅

가상환경을 활성화합니다. 꼭 venv을 쓰지 않아도 괜찮습니다.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

### 커밋 전 확인 사항

푸시 전 아래 작업이 필요합니다. (`black`, `pylint`, `pip freeze`)

```sh
black -v .
pylint --disable=all --enable=F,E,unreachable,duplicate-key,unnecessary-semicolon,global-variable-not-assigned,unused-variable,binary-op-exception,bad-format-string,anomalous-backslash-in-string,bad-open-mode --disable=E0402 --msg-template='{line}:{column} ({category}) {symbol}:{msg}' --reports=n --output-format=text \**/_.py
pip3 freeze > requirements.txt
```

pylint 수행 결과가 무조건 만점(10.0/10)이 나와야 합니다.

### 그 외 개발 참고사항

#### 디펜던시 체크

requirements.txt에 포함된 `pipdeptree`로 디펜던시 체크가 가능합니다.

#### 로또6/45 관련 data (참고용)

##### Request body (3 tickets)

```python
 data = {
    "round": 777,
    "direct": "172.17.20.52",
    "nBuyAmount": str(1000 * cnt),
    "param": '[{"genType":"0","arrGameChoiceNum":null,"alpabet":"A"},{"genType":"0","arrGameChoiceNum":null,"alpabet":"B"},{"genType":"0","arrGameChoiceNum":null,"alpabet":"C"}]',
    # "ROUND_DRAW_DATE": "2021/06/12", # 안넣어도 작동함
    # "WAMT_PAY_TLMT_END_DT": "2022/06/13", # 안넣어도 작동함
    "gameCnt": cnt,
}
```

##### Response body (3 tickets)

```python
result example:
{
    "loginYn": "Y",
    "result": {
        "oltInetUserId": "00NNNNNNN",
        "issueTime": "hh:mm:ss",
        "issueDay": "yyyy/MM/dd",
        "resultCode": "100",
        "barCode4": "nnnnn",
        "barCode5": "nnnnn",
        "barCode6": "nnnnn",
        "barCode1": "nnnnn",
        "barCode2": "nnnnn",
        "barCode3": "nnnnn",
        "resultMsg": "SUCCESS",
        "buyRound": "950",
        "arrGameChoiceNum": [
            "A|nn|nn|nn|nn|nn|nn3", // TODO: what is '3'?
            "B|nn|nn|nn|nn|nn|nn3",
            "C|nn|nn|nn|nn|nn|nn3"
        ],
        "weekDay": "월",
        "payLimitDate": None,
        "drawDate": None,
        "nBuyAmount": 3000
    }
}
```
