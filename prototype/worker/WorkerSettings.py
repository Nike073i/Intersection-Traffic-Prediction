from dataclasses import dataclass

@dataclass
class WorkerSettings:
    group : str
    name : str
    block: int
    model_type: str
    horizon: int
    lag: int
    base_path: str
    csv_path: str
