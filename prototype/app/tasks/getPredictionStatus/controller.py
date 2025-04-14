from .models import Query, Response

async def controller(query_handler, request):
    query = Query(request.prediction_id)
    result = await query_handler(query)
    return Response(result.prediction_id, result.crossroad_id, result.status, result.time, result.situations) if result else None