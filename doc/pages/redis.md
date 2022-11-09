# redis

## connect

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/redis/connect.py) -->
<!-- The below code snippet is automatically added from ../../python/redis/connect.py -->
```py
import os
from redis import Redis

redis = Redis(host=os.environ.get("REDIS_HOST", "localhost"),
              port=os.environ.get("REDIS_PORT", 6379),
              db=0)

print(redis.get("hello"))
```
<!-- MARKDOWN-AUTO-DOCS:END -->


