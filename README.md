# 비공식 동행복권 API

[동행복권](https://dhlottery.co.kr/) 사이트를 터미널에서 이용할 수 있게 랩핑한 API입니다.

### 설치 밎 사용법

```sh
pip install dhapi # pip 최신 버전을 권장합니다: pip install --upgrade pip
dhapi buy_lotto645 --help # 로또6/45 구매 도움말 보기
dhapi buy_lotto645 -q # 자동모드로 5장 구매
```

## 구현된 기능

- [로또 6/45](https://dhlottery.co.kr/gameInfo.do?method=gameMethod&wiselog=H_B_1_1)
    - 자동 구매 1 ~ 5장

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

### 이메일로 결과 전송 하기

`-e` 플래그로 수신할 이메일을 지정합니다. 이렇게 하면 **콘솔에 결과가 출력되지 않고 지정한 이메일로 전송됩니다.** 아래 세팅이 추가적으로 필요합니다.

무료로 이메일을 보내기 위해 [Mailjet](https://www.mailjet.com/)을 사용합니다. 가입한 후, API KEY, SECRET KEY 를 발급합니다 (https://app.mailjet.com/account/apikeys).

키 정보를 ~/.dhapi/credentials 파일에 다음과 같이 기입합니다.

```text
[default]
username = "dhlotter_id"
password = "dhlotter_pw"
mailjet_api_key = "YOUR_API_KEY"
mailjet_api_secret = "YOUR_SECRET_KEY"
mailjet_sender_email = "YOUR_MAILJET_EMAIL"
[another_profile]
...
```

필요한 프로필에만 세팅하면 됩니다.

> [!IMPORTANT]  
> 위 세팅대로 따라온다면 결과 이메일이 아주 높은 확률로 스팸 메일함에 들어갑니다. 이럴 경우 해당 메일을 찾아서 '스팸이 아님' 체크를 해야 이후 메일들이 일반 메일함에 들어갑니다.

> [!WARNING]  
> `mailjet_sender_email` 값은 '발신 이메일 주소'로 활용되며, Mailjet 회원가입에 사용한 이메일이 아닐 경우 추가 세팅을 해야됩니다.
>
> 따로 세팅을 하지 않은 상태로 별도의 이메일을 기입하게 되면, 실제 메일이 발송되지 않고 'Senders and domains page'를 확인하라는 안내 메일을 받게 됩니다.

## 기여하기

기여는 대환영입니다! [CONTRIBUTING.md](/docs/CONTRIBUTING.md) 파일을 참고해주세요.

## 기부하기

이 프로그램을 사용해서 1등에 당첨된다면, 저에게 꼭 1000만원을 기부해주시길 바랍니다.

<img alt="Toss Donation QR Code" src="./docs/toss_donation_qr.png" width="300" />

그리고 딱히 당첨된 적은 없지만 그래도 커피를 사주고 싶다면, 절대 망설이지 마십시오.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/roeniss)
