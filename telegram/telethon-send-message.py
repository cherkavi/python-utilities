from telethon.sync import TelegramClient, events
from telethon import functions, types
from telethon.tl.types import InputPeerUser
from telethon.tl.functions.channels import JoinChannelRequest
import sys
import os

def read_env_variables():
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    api_session = os.getenv('TELEGRAM_SESSION_DB')
    if api_id is None :
        raise ValueError("TELEGRAM_API_ID is not set.")    
    if api_hash is None:
        raise ValueError("TELEGRAM_API_HASH is not set.")  
    if api_session is None:
        api_session = 'current_telegram_connection'
    return (api_id, api_hash, api_session)

# if __name__ == "__main__":
api_id, api_hash, session_name = read_env_variables()

client = TelegramClient(session_name, api_id, api_hash)   # with TelegramClient('name', api_id, api_hash) as :
client.start()

## get information about myself
print(client.get_peer_id('me'))
print(client.download_profile_photo('me'))

##    Get contact information
# alias: str = "John Doe"
# alias: str = "phone number of the contact from entities table"
# recipient_id=client.get_peer_id(alias)
# print(recipient_id)


##    Print all contacts, contact list
# result = client(functions.contacts.GetContactsRequest(hash=0))    
# for user in result.users:
#     print(f"Name: {user.first_name} {user.last_name}, Username: {user.username}, Id: {user.id}, Phone: {user.phone}")


##    Create/Add new contact
# new_contact = types.InputPhoneContact(
#     client_id=0, # A unique identifier for this request (can be any int)
#     phone='+491605553999', # The user's phone number (must include country code if not local)
#     first_name='Metallbau-Treppenbau',
#     last_name=''
# )
# result = client(functions.contacts.ImportContactsRequest(contacts=[new_contact,]))
# print(result)
# print(result.imported)
# for each_user in result.users:
#     print(each_user)
#     print(each_user.id)
#     print(each_user.first_name)
#     print(each_user.phone)


##    Send message to myself
# client.send_message('me', 'Hello, myself!')
# client.send_message(recipient_id, 'Hello, myself!')


##    Send text message to: https://web.telegram.org/a/#732369999
#                                               user.id
# alias: str = "Name from my contact"
# alias: str = "phone number of the contact from entities table"
# client.send_message(alias, 'Hello!')


##    Send message with image to: https://web.telegram.org/a/#732369999
#                         via lib/python3.12/site-packages/telethon/client/messages.py
# client.parse_mode = 'html'
# contact_id = 732369999
# html_message = 'this is <b>temp</b> <a href="https://google.com">file</a>'
# image_path='/tmp/5300846472515939035.jpg'
# client.send_file(contact_id, file=image_path, caption=html_message)


##    Send message with image to: https://web.telegram.org/a/#732369999
#                                                             user.id
# contact_id = 732369999
# alternative_way_of_setting_id: contact = client.get_input_entity('contact_username_or_phone_number')
# contact = InputPeerUser(contact_id, 0)
# image_path='/tmp/5300846472515939035.jpg'
# html_message = '<b>Hello!</b> This is a <i>formatted</i> message with an <u>image</u>.'
# client.send_message( entity=contact, message=html_message, parse_mode='html', file=image_path)


##     Request to connect user to channel, subsribe user to channel
# channel_id=-10031226999999
# channel_entity = client.get_input_entity(channel_id)
# print(channel_entity)
# user_id=16999999999
# user_entity = client.get_input_entity(user_id)
# print(user_entity)
# result = client(functions.channels.InviteToChannelRequest(channel=channel_entity,users=[user_entity]))
# print(result)
# print(result.updates)
# print(result.updates.updates)
# print(result.updates.users)
# print(result.updates.chats)
# print(result.missing_invitees)


##      Get all contacts from group
# groups = ["group1","group2","group3"]
# for each_group in groups:
#     client(JoinChannelRequest(each_group))
#     
#     for user in client.get_participants(each_group, aggressive=True)
#         print(user)
#         print(user.id)
#         print(user.first_name)
#         print(user.last_name)
#         print(user.access_hash)
#         print(user.username)
#         print(user.phone)
#         print(user.bot)
#         print(user.verified)
#         


## mandatory disconnect
client.disconnect()


