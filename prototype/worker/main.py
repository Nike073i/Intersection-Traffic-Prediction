import dotenv
import asyncio
from .prediction_worker_factory import prediction_worker_factory
from .WorkerSettings import WorkerSettings
from redis_client import RedisSettings

def read_configuration():
    redis_host_key="REDIS_HOST"
    redis_port_key="REDIS_PORT"

    worker_group_key="WORKER_GROUP"
    worker_name_key="WORKER_NAME"
    worker_block_key="WORKER_BLOCK"

    predict_model_type_key="PREDICT_MODEL_TYPE"
    predict_horizon_key="PREDICT_HORIZON"
    predict_lag_key="PREDICT_LAG"
    predict_base_path_key="PREDICT_BASE_PATH_MODEL"
    
    local_data_path_key="LOCAL_DATA_PATH"

    values = dotenv.dotenv_values()

    def get_redis_settings():
        return RedisSettings(values[redis_host_key], values[redis_port_key])
    
    def get_worker_settings():
        return WorkerSettings(
            values[worker_group_key], 
            values[worker_name_key], 
            int(values[worker_block_key]),
            values[predict_model_type_key],
            int(values[predict_horizon_key]),
            int(values[predict_lag_key]),
            values[predict_base_path_key],
            values[local_data_path_key]
        )

    return get_redis_settings, get_worker_settings

if __name__ == "__main__":
    get_redis_settings, get_worker_settings = read_configuration()
    redis_settings = get_redis_settings()
    worker_settings = get_worker_settings()
    worker = prediction_worker_factory(redis_settings, worker_settings)

    try:
        asyncio.run(worker())
    except KeyboardInterrupt:
        print("Задача прервана пользователем.")
