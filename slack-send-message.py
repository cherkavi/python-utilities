### send message to slack channel
## two env variables are expected:
## * SLACK_DEFAULT_CHANNEL - name of the channel (#) or id
## * SLACK_ACCESS_TOKEN - OAuth token of application, [how to](https://github.com/CircleCI-Public/slack-orb/wiki/Setup):
##   1. create new slack application
##   2. add rights to application: chat:write, chat:write.public, files:write
##   3. obtain oauth token, install/add to workspace ( select workspace where app should be )
##   4. check application in slack, add application as a member to one of the channel


## need to install slack library:
# pip3 install slack_sdk
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initialize the Slack API client
slack_token = os.environ.get("SLACK_ACCESS_TOKEN")
client = WebClient(token=slack_token)

# Define the channel and message
# channel = "#udacity-aws-devops"
# channel = "C05DY0xxxx"  # slack channel id
channel = os.environ.get("SLACK_DEFAULT_CHANNEL")
message = "Hello, Slack!"

# Send the message
try:
    response = client.chat_postMessage(channel=channel, text=message)
    print("Message sent successfully")
except SlackApiError as e:
    print(f"Failed to send message: {e.response['error']}")
