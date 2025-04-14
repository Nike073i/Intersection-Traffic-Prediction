from dataclasses import dataclass
from typing import List, Optional


@dataclass
class QueryResult:
    prediction_id: str
    status: str
    crossroad_id: Optional[int] = None
    time: Optional[List[str]] = None
    situations: Optional[List[int]] = None
