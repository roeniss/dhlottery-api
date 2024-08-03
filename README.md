# 비공식 동행복권 API

[![PyPI version](https://badge.fury.io/py/dhapi.svg)](https://badge.fury.io/py/dhapi)

[동행복권](https://dhlottery.co.kr/) 사이트를 터미널에서 이용할 수 있게 랩핑한 API입니다.

https://github.com/roeniss/dhlottery-api/raw/main/docs/demo.mp4

### 설치 밎 사용법

```sh
pip install dhapi --upgrade # pip 최신 버전을 권장합니다: pip install --upgrade pip
dhapi --help # 기본 도움말 보기 
dhapi buy-lotto645 --help # '로또6/45' 구매 명령어의 도움말 보기
dhapi buy-lotto645 -y # '로또6/45' 자동모드로 5장 구매 & 확인절차 스킵
```

## 구현된 기능들

- [로또6/45 구매](https://dhlottery.co.kr/gameInfo.do?method=gameMethod&wiselog=H_B_1_1) (`buy-lotto645`)
    - 자동, 수동, 반자동 모드로 구매 가능합니다.
    - 한 번에 최대 5장까지 구매 가능합니다.
    - 매주 최대 5장까지 구매 가능합니다 (동행복권 측의 온라인 구매 관련 정책입니다).
- [예치금 현황 조회](https://dhlottery.co.kr/userSsl.do?method=myPage) (`show-balance`)
    - 현재 보유한 예치금 정보를 조회합니다.
- [고정 가상계좌 입금을 위한 세팅](https://dhlottery.co.kr/userSsl.do?method=myPage) (`assign-virtual-account`)
    - 개인에게 할당된 가상계좌에 입금하는 형태로 예치금을 충전할 수 있습니다. 이 때 얼마를 입금할건지 사이트에서 미리 선택해두어야 하는데, 이 작업을 대신 수행합니다.
    - 입금은 직접 진행해야 합니다.
    - 간편 충전 기능은 구현되지 않았습니다.

### 유틸성 기능들

- 복수 프로필 지정
    - 두 개 이상의 프로필을 사용할 수 있습니다. 고급 설정 섹션을 참고해주세요.

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

## 기부하기

이 프로그램을 사용해서 1등에 당첨된다면, 저에게 꼭 1000만원을 기부해주시길 바랍니다.

그리고 딱히 당첨된 적은 없지만 그래도 커피를 사주고 싶다면, 절대 망설이지 마십시오.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/roeniss)

## 기여하기

기여는 대환영입니다! [CONTRIBUTING.md](/docs/CONTRIBUTING.md) 파일을 참고해주세요.
