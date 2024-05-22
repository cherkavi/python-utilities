from jira import JIRA
from typing import List, Dict
from jira.resources import (Comment, Issue)
import os
import sys
import datetime

STRICT: bool = "only-my-comments" in sys.argv[1:]
TODAY: bool = "only-today" in sys.argv[1:]
PROJECT_NAME = "EXTRACT"
USER_NAME = "my-number-245"

def remove_before_minus(s):
    return "jira "+s.split('-')[1]+" # "

def add_prefix_to_each_line(s: str):
    prefix = "   "
    return prefix + prefix.join(s.splitlines(True))

# curl -H "Authorization: Bearer ${JIRA_TOKEN}" -X GET ${JIRA_URL}/rest/api/2/myself | jq .
jira = JIRA(server=os.getenv('JIRA_URL'), 
            token_auth=os.getenv('JIRA_TOKEN'))

class Result:
    def __init__(self, issue: Issue, comments: List[Comment]):
        self.issue = issue
        self.comments = comments

results: List[Result] = []

for ticket in jira.search_issues(f'project = {PROJECT_NAME} AND resolution = Unresolved AND text ~ {USER_NAME} order by updated DESC'):
    comments = ticket.fields.comment.comments
    if STRICT:
        comments = [each_comment for each_comment in comments if "q453337" in each_comment.body]
    if TODAY:
        comments = [each_comment for each_comment in comments if each_comment.updated.startswith(datetime.datetime.now().strftime("%Y-%m-%d"))]
    if len(comments) > 0:
        comments = sorted(comments, key=lambda x: x.updated, reverse=False)
        results.append(Result(issue=ticket, comments=comments))

results: List[Result] = sorted(results, key=lambda x: x.comments[len(x.comments)-1].updated, reverse=False)

for result in results:
    ticket: Issue = result.issue
    comments: List[Comment] = result.comments

    print("##############################")
    print(remove_before_minus(ticket.key), ticket.fields.summary)
    print(comments[len(comments)-1].updated)
    print("##############################")
    for each_comment in comments:
        print(f"{each_comment.updated}  -  {each_comment.author.displayName} \n {add_prefix_to_each_line(each_comment.body)}\n--------------")    
