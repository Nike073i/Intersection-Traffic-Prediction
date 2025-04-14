from fastapi_setup import ResponseBuilder
from ..models import Response

def create_answer(response: Response):
   responseBuilder = ResponseBuilder()
   if not response:
      responseBuilder.not_found()
   else:
      responseBuilder.ok(response)
   return responseBuilder.build()