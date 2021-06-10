## 개발 가이드

### pre

가상환경 활성화

````sh
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

pylint는 만점(10.00/10)이어야 한다.
````
