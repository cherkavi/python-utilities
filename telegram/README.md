# telegram
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

python3 send-message.py
```


### telegram info
```sh
sqlite3 name.session
.tables

# get all contacts 
select * from entities;
```