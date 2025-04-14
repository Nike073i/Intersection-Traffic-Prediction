from functools import partial
from fastapi import Depends
from fastapi_setup import http_endpoint, get_redis_client 
from .http import read_request, create_answer 
from .query_handler import query_handler
from .controller import controller

def create_use_case(redis_client = Depends(get_redis_client)):
    handler = partial(query_handler, redis_client)
    return partial(controller, handler)

endpoint = http_endpoint(read_request, create_use_case, create_answer)