from ..models.Request import Request

def read_request(prediction_id: str):
    return Request(prediction_id)
