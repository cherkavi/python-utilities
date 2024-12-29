from telethon.sync import TelegramClient, events
import sys
import os

def read_env_variables():
    # Read variables from environment
    var1 = os.getenv('TELEGRAM_API_ID')
    var2 = os.getenv('TELEGRAM_API_HASH')

    # Check if the variables exist
    if var1 is None or var2 is None:
        raise ValueError("TELEGRAM_API_ID and/or TELEGRAM_API_HASH  are not set.")
    
    return (var1, var2)

if __name__ == "__main__":
    api_id, api_hash = read_env_variables()

    with TelegramClient('name', api_id, api_hash) as client:
        ## get information 
        # print(client.get_peer_id('me'))
        # print(client.download_profile_photo('me'))
        # print(client.get_peer_id(alias))

        ## send message to myself
        # client.send_message('me', 'Hello, myself!')
        
        ## send message to: https://web.telegram.org/a/#732369999
        # alias: str = "Name from my contact"
        # alias: str = "phone number of the contact from entities table"
        # client.send_message(alias, 'Hello!')

        ## send file 
        # lib/python3.12/site-packages/telethon/client/messages.py
        # client.parse_mode = 'html'
        # client.send_file('me', file='/tmp/5433727001103034538.jpg', caption='this is <b>temp</b> <a href="https://google.com">file</a>')
        
        ## mandatory disconnect
        client.disconnect()


