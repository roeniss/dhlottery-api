# DongHaeng Lottery API (Unofficial)

[동행복권](https://dhlottery.co.kr/) 사이트를 터미널에서 이용할 수 있게 랩핑한 API입니다.

Python 3.8 이상에서 설치해야 최신버전이 작동합니다.

## 구현된 기능

-   [로또 6/45](https://dhlottery.co.kr/gameInfo.do?method=gameMethod&wiselog=H_B_1_1)
    -   자동 구매 1 ~ 5장

## 설치 및 사용법

```sh
pip install dhapi
dhapi -h
dhapi buy_lotto645 -u $USER_ID -q
```

## 기여하기

기여는 대환영입니다! [CONTRIBUTING.md](/docs/CONTRIBUTING.md) 파일을 참고해주세요.
