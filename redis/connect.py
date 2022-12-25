import os
from redis import Redis

redis = Redis(host=os.environ.get("REDIS_HOST", "localhost"),
              port=os.environ.get("REDIS_PORT", 6379),
              db=0)

# for entry in redis.hgetall("table_1").values():
# redis.hset(name="table_1",key="key_1",value="value_1")
# redis.hdel("table_1", "key_1")

print(redis.get("hello"))
