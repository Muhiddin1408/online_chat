from redis import Redis
from conf.settings import REDIS_HOST, REDIS_PORT, CELERY_REDIS_DB


# Create a Redis connection
redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=CELERY_REDIS_DB)


class RedisCache:
    def set(key, value):
        data = redis.set(key, value)

        return data
    
    def get(key):
        data = redis.get(key)
        if data:
            return data.decode('utf-8')
        return None
    
    def delete(key):
        redis.delete(key)