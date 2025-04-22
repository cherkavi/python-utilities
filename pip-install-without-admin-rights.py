## how to install packages inside python to avoid admin lock 
# select your python version to download 
# curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
# curl https://bootstrap.pypa.io/pip/3.6/get-pip.py > get-pip.py
# copy to destination host 
# python get-pip.py

python3
import pip
pip.main(['install', 'stem']) # install package
# pip.main(['install', '-U', 'requests']) # update package
# pip.main(['uninstall ', '-y', 'requests']) # uninstall package
