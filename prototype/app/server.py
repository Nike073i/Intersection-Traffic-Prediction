from fastapi_setup.read_configuration import read_configuration
from redis_client import pool_factory
from .appBuilder import AppBuilder
from .tasks import create_tasks_module, GET_PREDICTION_STATUS_NAME

get_redis_settings = read_configuration()
redisSettins = get_redis_settings()
get_client = pool_factory(redisSettins)


builder = AppBuilder().add_module(create_tasks_module())
app = builder.build()