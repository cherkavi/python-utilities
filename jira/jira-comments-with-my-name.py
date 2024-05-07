from jira import JIRA
import os

def remove_before_minus(s):
    return "jira-"+s.split('-')[1]

def add_prefix_to_each_line(s: str):
    prefix = "   "
    return prefix + prefix.join(s.splitlines(True))

# curl -H "Authorization: Bearer ${JIRA_TOKEN}" -X GET ${JIRA_URL}/rest/api/2/myself | jq .
jira = JIRA(server=os.getenv('JIRA_URL'), 
            token_auth=os.getenv('JIRA_TOKEN'))

# ticket = jira.issue('IOO-6728')
for ticket in jira.search_issues('project = IVSOO AND status not in (Closed) AND text ~ "user-33" order by updated DESC'):
    print("##############################")
    print(remove_before_minus(ticket.key), ticket.fields.summary)
    print("##############################")
    comments = ticket.fields.comment.comments
    sorted(comments, key=lambda x: x.updated, reverse=True)
    for each_comment in comments:
        if each_comment.body.find("user-33") != -1:
            print(f"{each_comment.updated}  -  {each_comment.author.displayName} \n--- \n {add_prefix_to_each_line(each_comment.body)}\n--------------")    
