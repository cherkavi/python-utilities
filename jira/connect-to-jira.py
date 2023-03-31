from jira import JIRA

jira_url: str = ""
jira_username: str = ""
jira_password: str = ""
jira_issue_id: str = ""

options = {"server": str(jira_url)}
jira = JIRA(options=options, basic_auth=(jira_username, jira_password)) 

jira_issue = jira.issue(jira_issue_id)
print(jira_issue.fields.summary)
print(jira_issue.fields.issuetype.name)
