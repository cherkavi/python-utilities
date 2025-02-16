from telethon.sync import TelegramClient, events
from telethon import functions
from telethon.tl.types import InputPeerUser
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
        ## get information about myself
        # print(client.get_peer_id('me'))
        # print(client.download_profile_photo('me'))
        # print(client.get_peer_id(alias))


        ## Print the contacts
        # result = client(functions.contacts.GetContactsRequest(hash=0))    
        # for user in result.users:
        #     print(f"Name: {user.first_name} {user.last_name}, Username: {user.username}, Id: {user.id}, Phone: {user.phone}")


        ## send message to myself
        # client.send_message('me', 'Hello, myself!')


        ## send text message to: https://web.telegram.org/a/#732369999
        #                                               user.id
        # alias: str = "Name from my contact"
        # alias: str = "phone number of the contact from entities table"
        # client.send_message(alias, 'Hello!')


        ## send message with image to: https://web.telegram.org/a/#732369999
        #                         via lib/python3.12/site-packages/telethon/client/messages.py
        # client.parse_mode = 'html'
        # contact_id = 732369999
        # html_message = 'this is <b>temp</b> <a href="https://google.com">file</a>'
        # image_path='/tmp/5300846472515939035.jpg'
        # client.send_file(contact_id, file=image_path, caption=html_message)


        ## send message with image to: https://web.telegram.org/a/#732369999
        #                                               user.id
        # contact_id = 732369999
        # alternative_way_of_setting_id: contact = client.get_input_entity('contact_username_or_phone_number')
        # contact = InputPeerUser(contact_id, 0)
        # image_path='/tmp/5300846472515939035.jpg'
        # html_message = '<b>Hello!</b> This is a <i>formatted</i> message with an <u>image</u>.'
        # client.send_message( entity=contact, message=html_message, parse_mode='html', file=image_path)

        
        ## mandatory disconnect
        client.disconnect()


