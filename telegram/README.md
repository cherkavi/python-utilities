# telegram

## obtain telegram credentials
1. Visit the official Telegram website at my.telegram.org
2. Log in using your Telegram account phone number
3. Once logged in, click on "API development tools".
4. Fill out the form to create a new application:
   - Enter an App title and Short name
   - Select "Desktop" as the platform
   - You can leave the URL and Description fields blank
5. Click on "Create application".
6. After creation, you will see an "App configuration" screen that displays:
   - $TELEGRAM_API_ID (labeled as "App api_id")
   - $TELEGRAM_API_HASH (labeled as "App api_hash")

## Telegram library
* [git](https://github.com/alexander-akhmetov/python-telegram)
* [python telegram doc](https://python-telegram.readthedocs.io/latest/tutorial.html)
* [python pip](https://pypi.org/project/python-telegram/)

### installation
```sh
python3 -m virtualenv venv
source venv/bin/activate

pip3 install python-telegram
``` 

### start app
```sh
echo $TELEGRAM_API_ID
echo $TELEGRAM_API_HASH

python3 telegram-send-message.py
```


## Telethon library
* [git](https://github.com/LonamiWebs/Telethon)
* [doc](https://docs.telethon.dev/en/stable/)

### installation
```sh
python3 -m virtualenv venv
source venv/bin/activate

pip3 install telethon
``` 

### start app
```sh
echo $TELEGRAM_API_ID
echo $TELEGRAM_API_HASH

python3 telethon-send-message.py
```

### telegram info
```sh
sqlite3 name.session
.tables

# get all contacts 
select * from entities;
```

### possible error
```
OSError: libssl.so.1.1: cannot open shared object file: No such file or directory
```
solution 1:
```sh
locate libssl.so.1.1
# /snap/core18/2829/usr/lib/x86_64-linux-gnu/libssl.so.1.1
export LD_LIBRARY_PATH=/snap/core18/2829/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH

ldconfig -p | grep libssl
```
solution 2:
```sh
wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.24_amd64.deb
sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2.24_amd64.deb
rm libssl1.1_1.1.1f-1ubuntu2.24_amd64.deb
```
