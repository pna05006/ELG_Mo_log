#!/bin/bash
echo "PRESS [ENTER] TO INSTALLATION"
echo "IF YOU WANT TO CANCEL, PRESS [CTRL] + [C]"
DirPath=$(pwd -P)
read

cd ..
sh -c "chmod +x Mo_Log.sh"
sh -c "chmod +x Program_File/py_log_ex.sh"
sh -c "chmod +x Program_File/bbd_log_ex.sh"

if [ "${1}" != "-u" ]
then
    echo "[Update the package lists and upgrade them]"
    sudo apt-get update -y
    sudo apt-get upgrade -y
else
    echo ""
    echo "[Skip update & upgrade the package]"
    echo ""
fi

echo "[Install python3 and module]"

sudo apt-get install python3 python3-pip
echo ""
echo "Installed pip3 version"
pip3 --version
echo ""
pip3 install pathlib tqdm argparse openpyxl

git clone https://github.com/pandas-dev/pandas.git
cd pandas
python setup.py install

echo "[Python and module installation complete!]"

exit 0
