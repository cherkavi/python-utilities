# confluence

## confluence api

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/confluence/confluence-api.py) -->
<!-- The below code snippet is automatically added from ../../python/confluence/confluence-api.py -->
```py
# pip install atlassian-python-api

from atlassian import Confluence

confluence = Confluence(url="https://asc.ubsgroup.net", username="username", password="password")
print(confluence)

create_result = confluence.create_page(space="AD", title="remove me", body="checking confluence api")
print(create_result)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


