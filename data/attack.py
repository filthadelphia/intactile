from dataclasses import dataclass
from datetime import datetime, timedelta

from data.user import Plan

@dataclass
class Attack:
    IP: str = None
    Port: int = 80
    Time: int = 0
    Method: str = None
    StartDate: datetime = datetime.now()
    EndDate: datetime = StartDate + timedelta(seconds=Time)
    LoopDate: datetime = EndDate + timedelta(seconds=8)
    User: Plan = None
