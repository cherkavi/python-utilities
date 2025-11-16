import sys
import os
from telegram.client import Telegram
from telegram.text import Spoiler, Code
import time


def read_env_variables():
    # Read variables from environment
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')
    
    # Check if the variables exist
    if not api_id:
        raise ValueError("TELEGRAM_API_ID environment variable is not set.")
    if not api_hash:
        raise ValueError("TELEGRAM_API_HASH environment variable is not set.")
    if not phone:
        raise ValueError("TELEGRAM_PHONE environment variable is not set (e.g., +3169999999).")
    
    return (api_id, api_hash, phone)

def new_message_handler(update):
    # We want to process only text messages.
    message_content = update['message']['content'].get('text', {})
    message_text = message_content.get('text', '').lower()
    is_outgoing = update['message']['is_outgoing']

    if not is_outgoing and message_text == 'ping':
        chat_id = update['message']['chat_id']
        print(f'Ping has been received from {chat_id}')
        tg.send_message(chat_id=chat_id,text='pong',)

# if __name__ == "__main__":

api_id, api_hash, phone = read_env_variables()
tg = Telegram(api_id=api_id,api_hash=api_hash,phone=phone,database_encryption_key='db-password-example',files_directory='/tmp/.tdlib_files/')
tg.login()

## for reacting for incoming messages:
# tg.add_message_handler(new_message_handler)
# tg.idle()

## print myself
result = tg.get_me()
print(result.update)

## get user 
#      https://web.telegram.org/a/#27169999
user_id=27169999   # ! not a phone number 
result = tg.get_user(user_id)  
result.wait(); print(result.update)

result = tg.get_user_full_info(user_id)
result.wait(); print(result.update)

## send message
# result = tg.send_message(chat_id, Spoiler('Hello world!'))
result = tg.send_message(chat_id=user_id, text='Hello world!')
# Wait for the message to be sent
result.wait(); print(result.update)

if result.update and result.update.get('@type') == 'error':
    print(f"Error sending message: {result.update}")


tg.stop()

# tg.add_message_handler
# tg.add_update_handler
# tg.api_hash
# tg.api_id
# tg.application_version
# tg.authorization_state
# tg.bot_token
# tg.call_method
# tg.create_basic_group_chat
# tg.delete_messages
# tg.device_model
# tg.files_directory
# tg.get_authorization_state
# tg.get_chat
# tg.get_chat_history
# tg.get_chats
# tg.get_me
# tg.get_message
# tg.get_supergroup_full_info
# tg.get_user
# tg.get_user_full_info
# tg.get_web_page_instant_view
# tg.idle
# tg.import_contacts
# tg.library_path
# tg.login
# tg.parse_text_entities
# tg.phone
# tg.proxy_port
# tg.proxy_server
# tg.proxy_type
# tg.register_user
# tg.remove_update_handler
# tg.send_code
# tg.send_message
# tg.send_password
# tg.stop
# tg.system_language_code
# tg.system_version
# tg.use_message_database
# tg.use_secret_chats
# tg.use_test_dc
# tg.worker
