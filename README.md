# DongHaeng Lottery API (Unofficial)

```shell
❯❯❯ dhapi buy_lotto645

[Lotto645 Buy Request]
Game A: ['x', 'x', 'x', 'x', 'x', 'x']
Game B: ['x', 'x', 'x', 'x', 'x', 'x']
Game C: ['x', 'x', 'x', 'x', 'x', 'x']
Game D: ['x', 'x', 'x', 'x', 'x', 'x']
Game E: ['x', 'x', 'x', 'x', 'x', 'x']
----------------------
❓ 위와 같이 구매하시겠습니까? [Y/n] y
✅ 구매를 완료하였습니다.
[Lotto645 Buy Response]
------------------
Round:		1068
Barcode:	54095 53510 29208 58505 11515 12578
Cost:		5000
Numbers:
		A|01|05|28|33|35|45 (자동)
		B|01|13|14|38|40|41 (자동)
		C|02|28|30|32|36|39 (자동)
		D|20|25|32|33|34|41 (자동)
		E|14|26|28|31|35|45 (자동)
Message:	SUCCESS
----------------------
❯❯❯ echo Cool.
Cool.
```

[동행복권](https://dhlottery.co.kr/) 사이트를 터미널에서 이용할 수 있게 랩핑한 API입니다.

Python 3.8 이상에서 설치해야 최신버전이 작동합니다.

## 구현된 기능

- [로또 6/45](https://dhlottery.co.kr/gameInfo.do?method=gameMethod&wiselog=H_B_1_1)
  - 자동 구매 1 ~ 5장

## 사용법

### 계정 정보 세팅

`~/.dhapi/credentials` 파일에 username, password를 입력하면 자동으로 로그인합니다.
profile을 여러개 설정할 수 있습니다.

```shell
DHAPI_USERNAME=asdf
DHAPI_PASSWORD=****

mkdir -p ~/.dhapi
cd ~/.dhapi

echo "[default]" > credentials
echo username = $DHAPI_USERNAME >> credentials # username
echo password = $DHAPI_PASSWORD >> credentials # password (미리 복잡한 난수로 변경하시길 권장합니다)
```
```shell
DHAPI_USERNAME=qwer
DHAPI_PASSWORD=5678

cd ~/.dhapi

echo "" >> credentials
echo "[qwer]" >> credentials
echo username = $DHAPI_USERNAME >> credentials
echo password = $DHAPI_PASSWORD >> credentials
```

> `-u $USER_ID` 파라미터를 이용하면 명령어 실행 중 비밀번호를 입력받는 방법도 있지만, 권장하지 않습니다.

### 설치 밎 사용법

```shell
pip install --upgrade pip # pip 가 최신 버전이 아니면 dhapi 구버전이 깔리는 경우가 있습니다
pip install dhapi

dhapi -h

# 자동모드로 5장 구매
dhapi buy_lotto645 -q # profile: default
dhapi buy_lotto645 -q -p qwer # profile: qwer
```

## 기여하기

기여는 대환영입니다! [CONTRIBUTING.md](/docs/CONTRIBUTING.md) 파일을 참고해주세요.
