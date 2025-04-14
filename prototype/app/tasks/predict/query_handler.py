from .models import Query, QueryResult


async def query_handler(redis_client, get_time, generate_prediction_id, get_crossroad_type, query: Query):
    crossroad_id = query.crossroad_id
    time = get_time()
    prediction_id = generate_prediction_id(crossroad_id, time)

    was_set = await redis_client.hsetnx(prediction_id, "status", "accepted")

    if was_set:
        crossroad_type = await get_crossroad_type(crossroad_id)

        await redis_client.xadd(crossroad_type, { 
                "prediction_id": prediction_id,
                "time": time.isoformat(),
                "crossroad_id": crossroad_id
         })
        
    return QueryResult(prediction_id)
