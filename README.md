# DongHaeng Lottery API (Unofficial)

[동행복권](https://dhlottery.co.kr/) 사이트를 터미널에서 이용할 수 있게 랩핑한 API입니다.

현재 제게 필요한 기능이 [로또 6/45](https://dhlottery.co.kr/gameInfo.do?method=gameMethod&wiselog=H_B_1_1) 구매 뿐이라서 해당 부분만 구현되어 있습니다. 만약 다른 기능이 필요하시면 아래 가이드를 따라서 직접 개발하시거나, Github Issues를 통해 개발 요청을 등록해주시길 바랍니다.

## 설치 및 사용법

> 현재는 `로또645`를 `자동`으로 사는 기능뿐입니다. 갯수(`-c`)는 1에서 5사이로 조절할 수 있습니다. 한 주에 5장을 초과해서 사려고 하면 구매가 되지 않고 적절한 에러 메시지가 출력됩니다.
>
> 한 마디로, **현재 조작할 수 있는 옵션은 `-c` 뿐입니다.**

### Windows, Linux, MacOSX

macOS 말고 테스트를 안해봐서, 혹 작동하지 않는다면 Issues로 알려주시길 바랍니다.

```sh

pip install dhapi # 또는 pip3 install dhapi

# 이후 다음과 같이 사용하면 됩니다

dhapi -h # 도움말 출력

dhapi -U $YOUR_ID -P -K lotto645 -T buy -M auto -C 5  # 로또645를 - 산다 - 5장 - 자동발급으로
```

현재는 아쉽게도 -C 옵션 (1~5개) 말고는 조절할 수 있는 옵션이 없습니다.

### python

본 레포를 클론해서 dhapi.py를 실행시키는 방법으로도 사용하실 수 있습니다.

```sh
git clone https://github.com/roeniss/dhlottery-api
cd dhlottery-api/src/dhapi
pip3 install -r requirements.txt # 디펜던시를 전역으로 설치하고 싶지 않다면 사전에 가상환경을 활성화해주세요

# 이후 다음과 같이 사용하면 됩니다

python3 dhapi -h # 도움말 출력

dhapi -U $YOUR_ID -P -K lotto645 -T buy -M auto -C  # 로또6/45를 - 산다 - 5장 - 자동발급으로
```

### schedule

```sh
crontab -e

0 0,6-23 * * * PATH=$PATH:/opt/homebrew/bin && dhapi buy_lotto645 -q
```

## 같이 개발하기

기여는 대환영입니다! [CONTRIBUTING.md](/CONTRIBUTING.md) 파일을 참고해주세요.
