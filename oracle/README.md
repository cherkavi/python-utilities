# Oracle install library
```sh
# check your glibc version 
ldd --version

# download "Basic Package Zip" from from 
x-www-browser https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html

# create destination folder
ORACLE_DEST_FOLDER=/home/soft/oracle
mkdir -p $ORACLE_DEST_FOLDER
cd $ORACLE_DEST_FOLDER

mv ~/Downloads/instantclient-basic-linux*.zip .
unzip instantclient-basic-linux*.zip 
ls -l

ORACLE_CLIENT_VERSION=instantclient_23_7

echo "
export ORACLE_HOME=/path/to/oracle/instant-client
export LD_LIBRARY_PATH=$ORACLE_DEST_FOLDER/$ORACLE_CLIENT_VERSION:\$LD_LIBRARY_PATH
" >> ~/.bashrc
```
