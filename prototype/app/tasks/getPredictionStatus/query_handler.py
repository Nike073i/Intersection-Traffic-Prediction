from .models import Query, QueryResult

async def query_handler(redis_client, query: Query):
    data = await redis_client.hgetall(query.prediction_id)
    return QueryResult(prediction_id=query.prediction_id, **data) if len(data) else None
