# ELG_Mo_log
## WSL로 Ubuntu 설치
1. 파워쉘에서 아래 코드 실행 후 재부팅
```
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```
2. 파워쉘에서 아래 코드 입력으로 wsl로 ubuntu 설치(wsl2를 사용하고 싶으면 첫 줄 생략)
```
wsl --set-default-version 1
wsl --install -d Ubuntu-20.04
```
3. 설치가 완료되면 셀이 열림. 

Username과 password입력


설치완료

## How to use this package

### Preparation
1) Clone this repository to your Ubunto
2) 'ELG_Mo_log/Installation/python_install_setting.sh' file Permission setting 
```bash
chmod +x ELG_Mo_log/Installation/python_install_setting.sh
```

### Set-up
1) Installing python3 and library used
```bash
cd ELG_Mo_log/Installation/
./python_install_setting.sh
```
apt update & upgrade를 처음 실행하는거라 시간이 좀 걸린다. 그러다보니 apt upgrade 과정에서 가끔 중간에 멈춰보일때가 있는데 enter누르면 제대로 진행되는 것 같다.

if you don't want apt update & upgrade, run under code
but 처음 설치하자마자 이걸로 실행하면 설치 오류
```
cd ELG_Mo_log/Installation/
./python_install_setting.sh -u
```

### log파일 넣기
1) /ELG_Mo_log 폴더 안에 넣어야 한다.
2) UPDLPDCP코드 기반 필터링 모드의 경우 log파일을 /ELG_Mo_log폴더에 그대로 넣는다.
3) Cell&FRU 매칭 모드의 경우, /ELG_Mo_log 폴더 안에 하위 폴더를 하나 만들고 그 안에 로그파일들을 넣는다.

참고) 윈도우 탐색기에서 \\\wsl$ 경로를 입력하면 wsl 디렉토리에 쉽게 접근 가능하다

### RUN
반드시 /ELG_Mo_log폴더 안으로 이동 후 Mo_Log.sh을 실행한다.
```bash
cd /ELG_Mo_log
./Mo_Log.sh
```



