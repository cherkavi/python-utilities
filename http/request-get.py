import requests
response: requests.Response = requests.get(url, cookies={"PHPSESSID": php_session_id })`
return response.json().get("user_id", None)
