# ELG_Mo_log

## How to use this package

### Preparation
1) Clone this repository to your Ubunto
2) 'ELG_Mo_log/Installation/python_install_setting.sh' file Permission setting 
```bash
chmod +x python_install_setting.sh
```

### Set-up
1) Installing python3 and library used
```bash
cd ELG_Mo_log/Installation/
./python_install_setting.sh
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



