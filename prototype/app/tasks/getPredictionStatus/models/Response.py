from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Response:
    prediction_id: str
    crossroad_id: int
    status: str
    time: Optional[List[str]]
    situations: Optional[List[int]]