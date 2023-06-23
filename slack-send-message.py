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
