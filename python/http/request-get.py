import requests
response: requests.Response = requests.get(url, cookies={"PHPSESSID": php_session_id }, headers={"x-api-key": self._api_key})`
return response.json().get("user_id", None)
