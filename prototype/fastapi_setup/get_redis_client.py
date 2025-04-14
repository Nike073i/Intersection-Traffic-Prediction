from fastapi import Depends
from redis_client import pool_factory
from .read_configuration import read_configuration

def init_redis_pool(get_redis_settings = Depends(read_configuration)):
    redis_settings = get_redis_settings()
    return pool_factory(redis_settings)

def get_redis_client(client_factory = Depends(init_redis_pool)):
    return client_factory()