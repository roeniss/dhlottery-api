## 개발 가이드

### pre

가상환경 활성화

```sh
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

### post

푸시 전 아래 과정 필요

```sh
black -v .
pylint --disable=all --enable=F,E,unreachable,duplicate-key,unnecessary-semicolon,global-variable-not-assigned,unused-variable,binary-op-exception,bad-format-string,anomalous-backslash-in-string,bad-open-mode --disable=E0402 --msg-template='{line}:{column} ({category}) {symbol}:{msg}' --reports=n --output-format=text \*_/_.py
pip3 freeze > requirements.txt
```

pylint는 무조건 만점(10.00/10)이어야 한다.

### 기타

의존성 확인 : `pipdeptree` (show dependency tree)

### tmp

lotto645 body backup

```python
 data = {
    "round": self._getNextRound(),
    "direct": "172.17.20.52",
    "nBuyAmount": str(1000 * cnt),
    "param": '[{"genType":"0","arrGameChoiceNum":null,"alpabet":"A"},{"genType":"0","arrGameChoiceNum":null,"alpabet":"B"},{"genType":"0","arrGameChoiceNum":null,"alpabet":"C"}]',
    # 아래 두 값 안넣어도 되는 것으로 확인
    # "ROUND_DRAW_DATE": "2021/06/12",
    # "WAMT_PAY_TLMT_END_DT": "2022/06/13",
    "gameCnt": cnt,
}
```

response body from buying lotto645

```python
# result example:
# {
#     "loginYn": "Y",
#     "result": {
#         "oltInetUserId": "00NNNNNNN",
#         "issueTime": "hh:mm:ss",
#         "issueDay": "yyyy/MM/dd",
#         "resultCode": "100",
#         "barCode4": "nnnnn",
#         "barCode5": "nnnnn",
#         "barCode6": "nnnnn",
#         "barCode1": "nnnnn",
#         "barCode2": "nnnnn",
#         "barCode3": "nnnnn",
#         "resultMsg": "SUCCESS",
#         "buyRound": "950",
#         "arrGameChoiceNum": [
#             "A|nn|nn|nn|nn|nn|nn3", // TODO: what is '3'?
#             "B|nn|nn|nn|nn|nn|nn3",
#             "C|nn|nn|nn|nn|nn|nn3"
#         ],
#         "weekDay": "월",
#         "payLimitDate": None,
#         "drawDate": None,
#         "nBuyAmount": 3000
#     }
# }
```

TODO:

- todo 처리
- 사용법 정리 (to Readme) & 배포
- main 함수 쪽 정리
