from fastapi_setup import ResponseBuilder
from ..models import Response

def create_answer(response: Response):
   responseBuilder = ResponseBuilder()
   responseBuilder.ok(response)
   return responseBuilder.build()