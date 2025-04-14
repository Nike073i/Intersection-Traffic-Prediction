from .models import Query, Response

async def controller(query_handler, request):
    query = Query(request.crossroad_id)
    result = await query_handler(query)
    return Response(result.prediction_id)