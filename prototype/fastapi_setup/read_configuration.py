import dotenv
from redis_client import RedisSettings

def read_configuration():
    redis_host_key="REDIS_HOST"
    redis_port_key="REDIS_PORT"

    values = dotenv.dotenv_values()

    def get_redis_settings():
        return RedisSettings(values[redis_host_key], values[redis_port_key])


    return get_redis_settings