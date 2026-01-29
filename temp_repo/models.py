from enum import Enum
from typing import List, Optional
from datetime import datetime, time

class TokenSource(Enum):
    ONLINE = 1
    WALK_IN = 2
    PAID_PRIORITY = 3
    FOLLOW_UP = 4

class TokenStatus(Enum):
    ALLOCATED = 1
    CANCELLED = 2
    NO_SHOW = 3
    COMPLETED = 4

class Token:
    def __init__(self, id: str, patient_name: str, source: TokenSource, priority: int):
        self.id = id
        self.patient_name = patient_name
        self.source = source
        self.priority = priority  # Higher number = higher priority
        self.status = TokenStatus.ALLOCATED
        self.allocated_time: Optional[datetime] = None

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return f"Token(id={self.id}, patient={self.patient_name}, source={self.source.name}, priority={self.priority})"

class Slot:
    def __init__(self, doctor_id: str, start_time: time, end_time: time, max_capacity: int):
        self.doctor_id = doctor_id
        self.start_time = start_time
        self.end_time = end_time
        self.max_capacity = max_capacity
        self.allocated_tokens: List[Token] = []
        self.waitlist: List[Token] = []  # For overflow, but since hard limits, maybe not used

    @property
    def current_capacity(self) -> int:
        return len([t for t in self.allocated_tokens if t.status == TokenStatus.ALLOCATED])

    @property
    def is_full(self) -> bool:
        return self.current_capacity >= self.max_capacity

    def allocate_token(self, token: Token) -> bool:
        if self.is_full:
            return False
        self.allocated_tokens.append(token)
        token.allocated_time = datetime.now()
        return True

    def cancel_token(self, token_id: str) -> bool:
        for token in self.allocated_tokens:
            if token.id == token_id and token.status == TokenStatus.ALLOCATED:
                token.status = TokenStatus.CANCELLED
                return True
        return False

    def __repr__(self):
        return f"Slot(doctor={self.doctor_id}, time={self.start_time}-{self.end_time}, capacity={self.current_capacity}/{self.max_capacity})"

class Doctor:
    def __init__(self, id: str, name: str, slots: List[Slot]):
        self.id = id
        self.name = name
        self.slots = slots

    def get_slot(self, start_time: time) -> Optional[Slot]:
        for slot in self.slots:
            if slot.start_time == start_time:
                return slot
        return None

    def __repr__(self):
        return f"Doctor(id={self.id}, name={self.name}, slots={len(self.slots)})"
