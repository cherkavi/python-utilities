import os
import os.path
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/chat.messages.readonly']

def get_credentials(path_to_credentials:str):
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists(path_to_credentials):
        try:
            creds = Credentials.from_authorized_user_file(path_to_credentials, SCOPES)
        except:
            print("no credentials provided")
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This triggers the CLI-based auth flow
            flow = InstalledAppFlow.from_client_secrets_file(
                path_to_credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(path_to_credentials, 'w') as token:
            token.write(creds.to_json())
    return creds

def search_messages(path_to_credentials:str, query:str):
    creds = get_credentials(path_to_credentials=path_to_credentials)
    service = build('chat', 'v1', credentials=creds)

    print(f"Searching for: {query}...")
    
    # Note: The Chat API primarily searches within specific "Spaces"
    # To list messages, you usually need a space name (e.g., 'spaces/XXXXXXXX')
    # This example lists spaces first to find where to search
    spaces_result = service.spaces().list().execute()
    spaces = spaces_result.get('spaces', [])

    if not spaces:
        print('No spaces found.')
        return

    for space in spaces:
        print(f"\nChecking Space: {space.get('displayName')} ({space.get('name')})")
        # List messages in this space
        messages_result = service.spaces().messages().list(parent=space.get('name')).execute()
        messages = messages_result.get('messages', [])
        
        for msg in messages:
            if query.lower() in msg.get('text', '').lower():
                print(f" - Found: {msg.get('text')}")

if __name__ == '__main__':
    # Check if at least one argument was provided
    if len(sys.argv) < 2:
        print("Error: enter path to the credentials ")
        sys.exit(1)
    path_to_credentials = sys.argv[1]
    if len(sys.argv) < 3:
        print(f"Error: enter query to search :{sys.argv}")
        sys.exit(2)    
    search_term = " ".join(sys.argv[2:])
    
    search_messages(path_to_credentials, search_term)