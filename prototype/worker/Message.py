from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class Message:
    id: str
    prediction_id: str
    time: datetime
    crossroad_id: UUID
