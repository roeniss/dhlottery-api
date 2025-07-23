# 개발 가이드

## 배경지식

### 작동 방식

동행복권 사이트는 `JSESSIONID`를 이용하여 유저를 인증합니다. 본 API에서는 `requests`를 이용해 로그인한 후 `JSESSIONID`를 메모리에 저장해 복권 구매에 활용합니다.

### 트러블슈팅 가이드

#### main.py 가 실행이 안될 때

`PYTHONPATH`를 아래와 같이 지정해보세요.

```sh
cd ..
PYTHONPATH=./src/ python3 src/dhapi/main.py buy_lotto645 -q
```

### PR 전 확인사항

아래 명령어를 통하여 컨벤션을 준수하는지 확인합니다.

```sh
make lintfmt
make check
make test
```

### 배포

이 작업은 메인테이너가 진행합니다.

1. main 브랜치의 최신 커밋에 태그를 추가합니다 (e.g., `git tag "v4.0.8"`)
2. publish workflow 를 실행합니다.

### 참고자료

#### Request body for Lottery645 (3 tickets)

```python
data = {
    "round": 777,
    "direct": "172.17.20.52",  # 안넣어도 작동하는 것 확인 X
    "nBuyAmount": str(1000 * 3),
    "param": '[{"genType":"0","arrGameChoiceNum":null,"alpabet":"A"},{"genType":"0","arrGameChoiceNum":null,"alpabet":"B"},{"genType":"0","arrGameChoiceNum":null,"alpabet":"C"}]',
    # "ROUND_DRAW_DATE": "2021/06/12",  # 안넣어도 작동하는 것 확인 O
    # "WAMT_PAY_TLMT_END_DT": "2022/06/13",  # 안넣어도 작동하는 것 확인 O
    "gameCnt": 3,
}
```

#### Response body for Lottery645 (3 tickets)

```python
# result example:
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
            "A|nn|nn|nn|nn|nn|nn3",  # Manual : 1, Combine : 2, Automatic : 3
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
