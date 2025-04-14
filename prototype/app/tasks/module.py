from fastapi import APIRouter
from .getPredictionStatus import endpoint as getEndpoint, ENDPOINT_NAME as GET_PREDICTION_STATUS_NAME
from .predict import endpoint as predictEndpoint, ENDPOINT_NAME as PREDICT_NAME


def create_tasks_module():
    router = APIRouter(prefix='/predicts', tags=['Predicts'])

    router.get('/{prediction_id:str}', name=GET_PREDICTION_STATUS_NAME)(getEndpoint)
    router.post('/{crossroad_id:int}', name=PREDICT_NAME)(predictEndpoint)

    return router
