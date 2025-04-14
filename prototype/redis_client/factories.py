import redis
from .RedisSettings import RedisSettings


def pool_factory(settings: RedisSettings):
    pool = redis.asyncio.ConnectionPool(host=settings.host, port=settings.port, decode_responses=True)

    def get_client():
        return redis.asyncio.Redis(connection_pool=pool)

    return get_client


def single_connection_factory(settings: RedisSettings):
    def get_client():
        return redis.Redis(host=settings.host, port=settings.port, decode_responses=True)
    return get_client