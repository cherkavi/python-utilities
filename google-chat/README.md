# read messages from GoogleChat

## installation python
```sh
sudo apt update && sudo apt install python3-pip -y
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## installation permissions
2. Google Cloud Console Configuration
Google requires a "Client ID" to verify your app. 
You must do this one-time setup in a browser:
1. Go to the Google Cloud Console and [Create a project](https://console.cloud.google.com/projectcreate) and enable the Google Chat API.
2. [Go to OAuth consent screen](https://console.cloud.google.com/auth/overview), set User Type to External, and add your email as a Test User.
   1. Project configuration
   2. App Information ( enter app name, enter you email ) 
   3. Audience - External 
3. [go to OAuth.Clients](https://console.cloud.google.com/auth/clients)
   1. create client
   2. application type: Select Desktop App, name it, and click Create.
   3. download as JSON, credentials.json
4. check the api enabling
   * https://console.cloud.google.com/apis/api/chat.googleapis.com/metrics
   * https://console.cloud.google.com/apis/api/chat.googleapis.com/hangouts-chat
    

## run next application for obtaining the permanent token
```python
from google_auth_oauthlib.flow import InstalledAppFlow
# https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces/list
SCOPES = ['https://www.googleapis.com/auth/chat.messages.readonly','https://www.googleapis.com/auth/chat.spaces.readonly']
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

# The fix is in these two arguments:
creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')
# creds = flow.run_console(port=0, access_type='offline', prompt='consent')

# Save the credentials for the next run
with open('/home/soft/google-chat-token.json', 'w') as token:
    token.write(creds.to_json())

## Access blocked: google-chat-reading-python-application has not completed the Google verification process
#  https://console.cloud.google.com/auth/audience
#> need to publish the application 
```

## check permanent token
```sh
access_token=$(cat /home/soft/google-chat-token.json | jq -r .token)

curl "https://oauth2.googleapis.com/tokeninfo?access_token=${access_token}"

curl -H "Authorization: Bearer ${access_token}" "https://chat.googleapis.com/v1/spaces"

# You can find this string in your client_secret.json file
project_id=$(cat /home/soft/credentials.json | jq -r .installed.project_id)
curl -H "Authorization: Bearer ${access_token}" "https://cloudresourcemanager.googleapis.com/v1/projects/${project_id}"
```

## run application 
```sh
python google_chat_search.py /home/soft/google-chat-token.json '#price'
```

