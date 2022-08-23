#!/bin/bash
echo "PRESS [ENTER] TO INSTALLATION"
echo "IF YOU WANT TO CANCEL, PRESS [CTRL] + [C]"
read

cd ..
sh -c "sudo chmod +x pylog.sh"
sh -c "sudo chmod +x bbd_log.sh"

echo "[Update the package lists and upgrade them]"
sudo apt-get update -y
sudo apt-get upgrade -y

echo "[Install python3 and module]"
sudo apt-get install Python3 python3-pip
echo ""
echo "Installed pip3 version"
pip3 --version
echo ""
pip3 install pandas numpy pathlib tqdm argparse
echo "[Python and module installation complete!]"