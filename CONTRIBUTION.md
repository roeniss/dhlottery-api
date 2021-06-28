# 개발 가이드

## 배경지식

### 작동 방식

동행복권 사이트는 `JSESSIONID`를 이용하여 유저를 인증합니다. 본 API에서는 `requests`를 이용해 로그인한 후 `JSESSIONID`를 메모리에 저장해 복권 구매에 활용합니다.

## 개발 환경 세팅

가상환경을 활성화해야 합니다. (꼭 venv을 쓰지 않아도 괜찮습니다)

```sh
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

## 커밋 전 확인 사항

### 린팅

푸시 전 린팅 작업이 필요합니다.

(black, pylint 설치 필요)

```sh
black -v .
find . -type f -name "*.py" | xargs pylint --disable=all --enable=F,E,unreachable,duplicate-key,unnecessary-semicolon,global-variable-not-assigned,unused-variable,binary-op-exception,bad-format-string,anomalous-backslash-in-string,bad-open-mode --disable=E0402 --msg-template='{line}:{column} ({category}) {symbol}:{msg}' --reports=n --output-format=text
```

pylint 수행 결과가 무조건 만점(10.0/10)이 나와야 합니다.

> 가상환경을 제대로 인식하지 못하면 `5:0 (error) import-error:Unable to import 'lib'`라는 에러와 함께 감점을 받을 수 있습니다. 이런 경우엔 [이 글](https://stackoverflow.com/a/53908601/8556340)을 참고해서 환경을 세팅해야 합니다.

### 디펜던시 체크

`pipdeptree`로 디펜던시 체크가 가능합니다. 불필요한 의존성을 확인 후 제거할 때 사용합니다.

확인 후에는 프리즈합니다.

```sh
pip3 freeze > requirements.txt
```

### 배포

pypi를 통해 배포합니다. ([pypi repository](https://pypi.org/project/dhapi/1.0.11/))

(build, setuptools, tween 필요)

`setup.py`에서 'version'을 적절하게 bump합니다.

그런데 pypi 저장소 토큰이 저한테 있으니까 지금은 저만 가능합니다.

```sh
python3 -m build --sdist &&\
    python3 -m build --wheel &&\
    twine check dist/* &&\
    twine upload dist/*
```

### etc

#### Request body for Lotter645 (3 tickets)

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

#### Response body for Lotter645 (3 tickets)

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
