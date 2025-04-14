from redis import ResponseError
from worker.WorkerSettings import WorkerSettings
from worker.Message import Message
from ctypes import Array
from datetime import timedelta, datetime
import json

def redis_service(get_client, worker_settings: WorkerSettings):
    redis = get_client()

    def get_messages() -> Array[Message]:
        responses = redis.xreadgroup(worker_settings.group, worker_settings.name, {worker_settings.model_type: '>'}, count=1, block=worker_settings.block)
        if not responses: return []

        # responses - [response] - bz count = 1
        # response - [stream, messages]
        messages = responses[0][1]

        def mapToMessage(msg):
            body = msg[1]
            time = datetime.fromisoformat(body['time'])
            return Message(
                id=msg[0],
                prediction_id=body['prediction_id'],
                time=time,
                crossroad_id=body['crossroad_id']
            )

        return map(mapToMessage, messages)

    def initialize():
        try:
            redis.xgroup_create(worker_settings.model_type, worker_settings.group, id='0', mkstream=True)
        except ResponseError as e:
            if "BUSYGROUP" in str(e):
                print("Группа уже существует, пропускаем создание")
            else:
                raise

    def save_prediction(prediction_id, crossroad_id, time, prediction):
        times = [ (time + timedelta(minutes=15 * i)).isoformat() for i in range(len(prediction)) ]

        redis.hset(prediction_id, mapping={
            "status": "completed",
            "crossroad_id": crossroad_id,
            "time": json.dumps(times),
            "situations": json.dumps(prediction.tolist())
        })

    def ack_message(id):
        redis.xack(worker_settings.model_type, worker_settings.group, id)

    return get_messages, ack_message, initialize, save_prediction