import redis
import os

# Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'db_redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

# Error handling for redis_client
try:
    redis_client.ping()
except redis.exceptions.ConnectionError as e:
    raise RuntimeError(f"Failed to connect to Redis: {str(e)}")
