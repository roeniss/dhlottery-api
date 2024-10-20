# 비공식 동행복권 API

[![PyPI version](https://badge.fury.io/py/dhapi.svg)](https://badge.fury.io/py/dhapi)

[동행복권](https://dhlottery.co.kr/) 사이트를 터미널에서 이용할 수 있게 랩핑한 API입니다.

https://github.com/user-attachments/assets/0be65454-8025-4fff-aa29-f88bc5948b43

### 설치 밎 사용법


```sh
# pip install dhapi --upgrade # pip 최신 버전을 권장합니다: pip install --upgrade pip
pip install -e . # 현재 프로젝트 경로의 src를 심볼릭 링크로 그대로 사용하는 패키지 설치하기옴
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

## 공유 라이브러리로 빌드하기
### 윈도우(build.bat)
```
@echo off
echo Building dhapi package into shared library
pip install cython
python setup.py build_ext --inplace
echo Build complete!
pause
```

```
build.bat
```

## 공유 라이브러리로 빌드하기
### wsl 우분투

0. 파이썬 환경 설치

miniconda 설치 후 환경 설치,  
cmake(pip, conda 모두)를 설치하지 않는다.

build-essential 설치.  

```
sudo apt update
sudo apt install build-essential
```

1. openjdk 설치

```
sudo apt update
sudo apt install openjdk-17-jdk
```
```
update-alternatives --config java
```
경로 등록.
```
nano ~/.bashrc
```
```
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```
```
source ~/.bashrc
```
jdk 설치 확인
```
java -version
```

2. gcc 컴파일러 설치

```
sudo apt update
sudo apt install gcc g++ libgcc-10-dev
```
gcc 설치 확인
```
gcc --version
which gcc
find /usr -name libgcc.a
```

3. android sdkmanager 설치

```
https://developer.android.com/tools/sdkmanager?hl=ko
```
를 따라서 폴더를 위치시킨 후, 등록.

```
nano ~/.bashrc
```

```
export ANDROID_SDK_ROOT=$HOME/android_sdk
export PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin
```
```
source ~/.bashrc
```
sdk manager 설치 확인
```
./sdkmanager --list
```
4. ndk, cmake, platform, system-images, build-tools 설치
```
sdkmanager --install "ndk;27.0.11718014"
sdkmanager --install "cmake;3.30.5"
sdkmanager --install "platforms;android-28" "platforms;android-29" "platforms;android-30" "platforms;android-31" "platforms;android-32" "platforms;android-33" "platforms;android-34" "platforms;android-35"
sdkmanager --install "system-images;android-28;default;arm64-v8a" "system-images;android-29;default;arm64-v8a" "system-images;android-30;default;arm64-v8a" "system-images;android-31;default;arm64-v8a" "system-images;android-32;default;arm64-v8a" "system-images;android-33;default;arm64-v8a" "system-images;android-34;default;arm64-v8a" "system-images;android-35;google_apis;arm64-v8a"
sdkmanager "build-tools;28.0.0" "build-tools;29.0.0" "build-tools;30.0.0" "build-tools;31.0.0" "build-tools;32.0.0" "build-tools;33.0.0" "build-tools;34.0.0" "build-tools;35.0.0"
```
```
sdkmanager --update
```
```
sdkmanager --licenses
```

5. 종합적인 환경 변수 등록  

- CMAKE 경로 추가:
```
echo 'export PATH="$PATH:/home/southglory/android_sdk/cmake/3.30.5/bin"' >> ~/.bashrc
source ~/.bashrc
```


- LIBRARY_PATH 추가: clang이 crtbegin_so.o 및 crtend_so.o 같은 파일을 찾을 수 있도록 라이브러리 경로를 설정.
```
export LIBRARY_PATH=/home/southglory/android_sdk/ndk/27.0.11718014/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/lib/aarch64-linux-android/28:$LIBRARY_PATH
```
- C_INCLUDE_PATH 및 CPLUS_INCLUDE_PATH 추가: clang이 NDK 관련 헤더 파일을 찾을 수 있도록 include 경로를 설정.
```
export C_INCLUDE_PATH=/home/southglory/android_sdk/ndk/27.0.11718014/sysroot/usr/include:$C_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=/home/southglory/android_sdk/ndk/27.0.11718014/sysroot/usr/include:$CPLUS_INCLUDE_PATH
```
- ANDROID_NDK_ROOT 및 NDK_ROOT: NDK와 관련된 설정을 명시적으로 해주기.
```
export ANDROID_NDK_ROOT=/home/southglory/android_sdk/ndk/27.0.11718014
export NDK_ROOT=$ANDROID_NDK_ROOT/toolchains/llvm/prebuilt/linux-x86_64
export SYSROOT=$NDK_ROOT/sysroot
```
- PATH 환경 변수에 NDK와 관련된 바이너리 경로 추가: NDK의 clang 및 clang++을 명령어로 쉽게 사용할 수 있도록 PATH에 추가.
```
export PATH=$NDK_ROOT/bin:$PATH
```

6. 빌드하기
```
python setup_for_android.py build_ext --inplace
```