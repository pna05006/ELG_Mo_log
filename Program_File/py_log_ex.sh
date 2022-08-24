#!/bin/bash
echo ""
echo "==============================="
echo "====== Start py_log Mode ======"
echo "==============================="

DirPath=$1
Dirlist=$(ls -d $DirPath/*/)
echo "[로그 폴더 목록]"
PS3='Select the folder >> '
select Di in $Dirlist
do
    folder=$(echo $Di | cut -d '/' -f2)
    if [ ${#folder} -eq 0 ]
    then
        echo "다시 선택해 주세요."
    else
        echo "The one you have selected is: $folder"
        break
    fi
done
echo -e "===============================\n[저장 파일 이름]"
read -p "Enter the file name(미입력시 폴더와 동일한 이름): " file
if [ ${#file} -eq 0 ]
then
file=$folder
fi

python3 Program_File/pylog.py $folder $file

exit 0