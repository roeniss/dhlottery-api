# DongHaeng Lottery API (Unofficial)

[동행복권](https://dhlottery.co.kr/) 사이트를 터미널에서 이용할 수 있게 랩핑한 API입니다.

Python 3.8 이상에서 설치해야 최신버전이 작동합니다.

## 구현된 기능

-   [로또 6/45](https://dhlottery.co.kr/gameInfo.do?method=gameMethod&wiselog=H_B_1_1)
    -   자동 구매 1 ~ 5장

## 사용법

### 사전준비: 계정 정보 세팅

`~/.dhapi_profile` 파일에 아이디와 패스워드를 입력하면 자동으로 로그인합니다. (`-p` 인자를 이용해 경로를 임의로 지정할 수도 있습니다)

    ```sh
    echo $USER_ID > ~/.dhapi_profile # 첫째 줄은 아이디
    echo $USER_PW >> ~/.dhapi_profile # 둘째 줄은 비밀번호 (미리 복잡한 난수로 변경하시길 권장합니다)
    ```

> `-u $USER_ID` 파라미터를 이용하면 명령어 실행 중 비밀번호를 입력받는 방법도 있지만, 권장하지 않습니다.

### 설치 밎 사용법:

```sh
pip install dhapi
dhapi -h
dhapi buy_lotto645 -q # 프로필 파일을 이용해 계정 정보 입력 & 자동모드로 5장 구매
```

## 기여하기

기여는 대환영입니다! [CONTRIBUTING.md](/docs/CONTRIBUTING.md) 파일을 참고해주세요.
