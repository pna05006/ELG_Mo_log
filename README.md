# ELG_Mo_log
## WSL로 Ubuntu 설치
1. 파워쉘에서 아래 코드 실행 후 재부팅
```
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```
2. 파워쉘에서 아래 코드 입력으로 wsl로 ubuntu 설치
```
wsl --install -d Ubuntu
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
if you don't want apt update & upgrade, run under code
```
cd ELG_Mo_log/Installation/
./python_install_setting.sh -u
```

### log파일 넣기
1) /ELG_Mo_log 폴더 안에 넣어야 한다.
2) UPDLPDCP코드 기반 필터링 모드의 경우 log파일을 /ELG_Mo_log폴더에 그대로 넣는다.
3) Cell&FRU 매칭 모드의 경우, /ELG_Mo_log 폴더 안에 하위 폴더를 하나 만들고 그 안에 로그파일들을 넣는다.

### RUN
반드시 /ELG_Mo_log폴더 안으로 이동 후 Mo_Log.sh을 실행한다.
```bash
cd /ELG_Mo_log
./Mo_Log.sh
```



