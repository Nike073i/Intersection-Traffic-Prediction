from redis_client import RedisSettings, single_connection_factory as redis_factory
from .WorkerSettings import WorkerSettings
from .prediction_worker import prediction_worker
from .redis_service import redis_service
from .load_traffic_forecaster import create_predictor, load_local_data


def prediction_worker_factory(redis_settings: RedisSettings, worker_settings: WorkerSettings):
    get_redis_client = redis_factory(redis_settings)
    get_messages, ack_message, initialize, save_prediction = redis_service(get_redis_client, worker_settings)
    initialize()

    get_prev_traffic = load_local_data(worker_settings.csv_path)
    predict = create_predictor(get_prev_traffic, worker_settings.horizon, worker_settings.lag, worker_settings.base_path)

    async def worker():
        return await prediction_worker(get_messages, predict, ack_message, save_prediction)

    return worker