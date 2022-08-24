#!/bin/bash
echo ""
echo "================================"
echo "====== Start bbd_log Mode ======"
echo "================================"

DirPath=$1
Dirlist=$(ls -d $DirPath/*.log)
echo "[로그 파일 목록]"
PS3='Select the log file >> '
select Di in $Dirlist
do
    file=$(echo $Di | cut -d '/' -f2)
    if [ ${#file} -eq 0 ]
    then
        echo "다시 선택해 주세요."
    else
        echo "The one you have selected is: $file"
        break
    fi
done
echo -e "===============================\n[저장 폴더 이름]"
read -p "Enter the foldor name(미입력시 파일과 동일한 이름): " folder
if [ ${#folder} -eq 0 ]
then
folder=$(echo $file | cut -d '.' -f1)
fi

python3 Program_File/bbd_log.py $file $folder

exit 0