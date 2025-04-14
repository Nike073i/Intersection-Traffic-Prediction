from ..models.Request import Request

def read_request(crossroad_id: int):
    return Request(crossroad_id)
