#!/bin/bash
echo "====== Welcome to MO_Log ====="

DirPath=$(dirname $0)
Dirlist=$(ls -d $DirPath/*/*ex.sh)

PS3='Select the .sh >> '
select Di in $Dirlist
do
    sh_file=$Di
    if [ ${#sh_file} -eq 0 ]
    then
        echo "다시 선택해 주세요."
    else
        echo "The one you have selected is: $sh_file"
        break
    fi
done

$sh_file $DirPath

exit 0