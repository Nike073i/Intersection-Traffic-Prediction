from datetime import datetime, timedelta
from functools import partial
from fastapi import Depends
from fastapi_setup import http_endpoint, get_redis_client 
from .http import read_request, create_answer 
from .query_handler import query_handler
from .controller import controller

def get_time():
    now = datetime.now() 
    remainder = now.minute % 15
    time = now + timedelta(minutes=15 - remainder)
    time.replace(second=0, microsecond=0, tzinfo=None)
    return time

def generate_prediction_id(crossroad_id, time):
    return f"{crossroad_id}_{time.strftime("%d%m%Y_%H%M")}"

async def get_crossroad_info(crossroad_id):
    return "common" if crossroad_id < 1000 else "another"


def create_use_case(redis_client = Depends(get_redis_client)):
    handler = partial(query_handler, redis_client, get_time, generate_prediction_id, get_crossroad_info)
    return partial(controller, handler)

endpoint = http_endpoint(read_request, create_use_case, create_answer)