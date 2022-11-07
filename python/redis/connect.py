import os
from redis import Redis

redis = Redis(host=os.environ.get("REDIS_HOST", "localhost"),
              port=os.environ.get("REDIS_PORT", 6379),
              db=0)

print(redis.get("hello"))
