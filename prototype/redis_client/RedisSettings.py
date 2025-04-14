from dataclasses import dataclass


@dataclass
class RedisSettings:
    host : str
    port : int