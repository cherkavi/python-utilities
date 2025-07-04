import sys
import json
import os
import requests

JIRA_URL = os.environ.get("JIRA_URL")
JIRA_TOKEN = os.environ.get("JIRA_TOKEN")
ISSUE_PREFIX="SPACE-"

if len(sys.argv) < 2:
    print("Usage: python jira-get-changelog-comments.py <ISSUE_KEY>")
    sys.exit(1)
ISSUE_KEY = sys.argv[1]

print("WARNING: This script will create many files in the current folder (one pair per description change).")
agree = input("Are you sure you want to continue? (Y/N): ").strip().lower()
if agree != 'y':
    print("Aborted by user.")
    sys.exit(0)
    

if not JIRA_URL or not JIRA_TOKEN:
    print("JIRA_URL and JIRA_TOKEN environment variables must be set.")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {JIRA_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.get(
    f"{JIRA_URL}/rest/api/2/issue/{ISSUE_PREFIX}{ISSUE_KEY}?expand=changelog",
    headers=headers
)
response.raise_for_status()
data = response.json()

for comment in data.get('fields').get('comment', {}).get('comments', []):
    created=comment.get("created")
    safe_created = created.replace(':', '-').replace('T', '_').replace('+', '_').replace('.', '_')
    from_path = f"{safe_created}.comment.txt"
    with open(from_path, 'w') as f_from:
        body=comment.get('body', '')
        f_from.write(body if body else "")

for history in data.get('changelog', {}).get('histories', []):
    created = history.get('created')
    if created:
        counter=0
        for item in history.get('items', []):            
            counter = counter+1
            print(f"{created}  - {item.get('field')}") 
            safe_created = created.replace(':', '-').replace('T', '_').replace('+', '_').replace('.', '_')
            from_path = f"{safe_created}.changelog.{counter}.from.txt"
            to_path = f"{safe_created}.changelog.{counter}.to.txt"
            if item.get('field') == 'description':
                with open(from_path, 'w') as f_from:
                    f_from.write(item.get('fromString', ''))
                with open(to_path, 'w') as f_to:
                    f_to.write(item.get('toString', ''))
            if item.get('field') == 'Comment':
                comment_from=item.get('from', '')
                comment_to=item.get('to', '')
                with open(from_path, 'w') as f_from:
                    f_from.write(comment_from if comment_from else '')
                with open(to_path, 'w') as f_to:
                    f_to.write(comment_to if comment_to else '')
