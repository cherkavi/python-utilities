# Oracle install library
## Download client
```sh
## official doc
# https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html

# check your glibc version 
ldd --version

# download "BasicLite Package Zip" from from 
# x-www-browser https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html
# wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip
# # alternative: wget https://download.oracle.com/otn_software/linux/instantclient/2340000/instantclient-basiclite-linux.x64-23.4.0.24.05.zip

# create destination folder
ORACLE_DEST_FOLDER=/home/soft/oracle
mkdir -p $ORACLE_DEST_FOLDER
cd $ORACLE_DEST_FOLDER

mv ~/Downloads/instantclient-basic-linux*.zip .
unzip instantclient-basiclite-linux*.zip 
ls -l
# check unzipped version
ORACLE_CLIENT_VERSION=instantclient_23_4

echo "
export ORACLE_HOME=$ORACLE_DEST_FOLDER/$ORACLE_CLIENT_VERSION
export LD_LIBRARY_PATH=$ORACLE_DEST_FOLDER/$ORACLE_CLIENT_VERSION:\$LD_LIBRARY_PATH
" >> ~/.bashrc

ll $LD_LIBRARY_PATH
ll $ORACLE_HOME

pip3 install --break-system-packages cx_Oracle
# python3 -m pip install --break-system-packages cx_Oracle --upgrade

## issues
# Cannot locate a 64-bit Oracle Client library: "/home/soft/oracle/instantclient_23_7/lib/libclntsh.so
# install basiclite of another version 
```

## install python package
```sh
pip3 install --break-system-packages cx_Oracle

## upgrade 
# python3 -m pip install --break-system-packages cx_Oracle --upgrade
```

## github workflow step for oracle installation
```json
      - name: Download Oracle Instant Client
        if: steps.cache-ext-file.outputs.cache-hit != 'true'
        run: |
          sudo apt-get update
          sudo apt-get install libaio1 wget unzip
          wget https://download.oracle.com/otn_software/linux/instantclient/2340000/instantclient-basiclite-linux.x64-23.4.0.24.05.zip
          # unzip instantclient-basiclite-linux.x64-23.4.0.24.05.zip
          # sudo mv instantclient_23_4 /opt/oracle  # libclntsh.so
          echo ">>>"$(pwd)
          # echo "export LD_LIBRARY_PATH=$(pwd)/instantclient_23_4:$LD_LIBRARY_PATH" >> $GITHUB_ENV

          rm -rf instantclient_23_4
          unzip -o instantclient-basiclite-linux.x64-23.4.0.24.05.zip

          python -m pip install --upgrade pip
          pip install -r db-to-csv/requirements.txt  # cx_Oracle
```
