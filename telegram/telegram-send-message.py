import sys
import os
from telegram.client import Telegram
from telegram.text import Spoiler, Code
import time


def read_env_variables():
    # Read variables from environment
    var1 = os.getenv('TELEGRAM_API_ID')
    var2 = os.getenv('TELEGRAM_API_HASH')
    var3 = os.getenv('TELEGRAM_PHONE')

    # Check if the variables exist
    if var1 is None or var2 is None or var3 is None:
        raise ValueError("TELEGRAM_API_ID and/or TELEGRAM_API_HASH and/or TELEGRAM_PHONE (+3169999999)  are not set.")
    
    return (var1, var2, var3)

if __name__ == "__main__":
    api_id, api_hash, phone = read_env_variables()
    tg = Telegram(
        api_id=api_id,
        api_hash=api_hash,
        phone=phone,
        database_encryption_key='db-password-example',
        files_directory='/tmp/.tdlib_files/',
    )
    tg.login()
    chat_id = 'me'
    # result = tg.send_message(chat_id, Spoiler('Hello world!'))
    result = tg.send_message(chat_id, text='Hello world!')
    
    result.wait()
    print(result.update)
    tg.stop()
