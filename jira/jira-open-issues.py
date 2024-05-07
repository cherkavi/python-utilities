from jira import JIRA
import os

def remove_before_minus(s):
    return "jira-"+s.split('-')[1]

# curl -H "Authorization: Bearer ${JIRA_TOKEN}" -X GET ${JIRA_URL}/rest/api/2/myself | jq .
jira = JIRA(server=os.getenv('JIRA_URL'), 
            token_auth=os.getenv('JIRA_TOKEN'))

# ticket = jira.issue('IOO-6028')
for ticket in jira.search_issues('assignee = currentUser() AND resolution = Unresolved'):
    print(f"{remove_before_minus(ticket.key):12}  {ticket.fields.summary:<50}")    
