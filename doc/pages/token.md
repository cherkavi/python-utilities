# token

## jwt

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/token/jwt.py) -->
<!-- The below code snippet is automatically added from ../../python/token/jwt.py -->
```py
# single sign on
# SSO token


# pip install PyJWT

import jwt

private_key = 'YOUR_PRIVATE_SSO_KEY'

def create_canny_token(user):
  user_data = {
    'avatarURL': user.avatar_url, # optional, but preferred
    'email': user.email,
    'id': user.id,
    'name': user.name,
  }
  return jwt.encode(user_data, private_key, algorithm='HS256')
```
<!-- MARKDOWN-AUTO-DOCS:END -->


