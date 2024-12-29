# telegram

## Telegram
* [git](https://github.com/alexander-akhmetov/python-telegram)
* [python telegram doc](https://python-telegram.readthedocs.io/latest/tutorial.html)
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

python3 send-message.py
```


## Telethon
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

### possible errors
```
OSError: libssl.so.1.1: cannot open shared object file: No such file or directory
```
```sh
locate libssl.so.1.1
# /snap/core18/2829/usr/lib/x86_64-linux-gnu/libssl.so.1.1
export LD_LIBRARY_PATH=/snap/core18/2829/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH

ldconfig -p | grep libssl
```