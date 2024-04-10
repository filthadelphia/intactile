from dataclasses import dataclass

@dataclass
class Plan:
    User: str
    UserID: int
    Expiration: str
    Cons: int