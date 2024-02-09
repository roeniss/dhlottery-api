# 비공식 동행복권 API

[동행복권](https://dhlottery.co.kr/) 사이트를 터미널에서 이용할 수 있게 랩핑한 API입니다.

### 설치 밎 사용법

```sh
pip install dhapi # pip 최신 버전을 권장합니다: pip install --upgrade pip
dhapi buy_lotto645 --help # 로또6/45 구매 도움말 보기
dhapi buy_lotto645 -q # 자동모드로 5장 구매
```

## 구현된 기능

-   [로또 6/45](https://dhlottery.co.kr/gameInfo.do?method=gameMethod&wiselog=H_B_1_1)
    -   자동 구매 1 ~ 5장

## 고급 설정

### 프로필 (계정) 설정

> [!NOTE] 최초 프로그램을 실행할 때 프로필 정보를 세팅하는 과정이 진행됩니다. 이 섹션에선 직접 프로필 정보 파일을 수정하는 법을 안내합니다.

`~/.dhapi/credentials` 파일을 사용해 프로필 정보를 수정하거나 여러 계정을 설정할 수 있습니다. toml 포맷을 사용하고 있으며, 아래와 같은 형식으로 작성할 수 있습니다.

```toml
[default]
username = "dhlotter_id"
password = "dhlotter_pw"
[another_profile]
username = "dhlotter_second_id"
password = "dhlotter_second_pw"
```

이후 `-p` 플래그로 프로필을 골라 사용합니다.

## 기여하기

기여는 대환영입니다! [CONTRIBUTING.md](/docs/CONTRIBUTING.md) 파일을 참고해주세요.

## 기부하기

이 프로그램을 사용해서 1등에 당첨된다면, 저에게 꼭 1000만원을 기부해주시길 바랍니다.

<img alt="Toss Donation QR Code" src="./docs/toss_donation_qr.png" width="300" />

그리고 딱히 당첨된 적은 없지만 그래도 커피를 사주고 싶다면, 절대 망설이지 마십시오.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/roeniss)
