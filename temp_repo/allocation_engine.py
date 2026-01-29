import heapq
from typing import List
from models import Doctor, Token, TokenSource, TokenStatus

class AllocationEngine:
    def __init__(self, doctors: List[Doctor]):
        self.doctors = doctors
        self.waiting_queue = []  # max heap: (-priority, token)

    def allocate_token(self, token: Token) -> bool:
        # Find the earliest available slot across all doctors
        best_slot = None
        best_time = None
        for doctor in self.doctors:
            for slot in doctor.slots:
                if not slot.is_full:
                    if best_time is None or slot.start_time < best_time:
                        best_time = slot.start_time
                        best_slot = slot
        if best_slot:
            best_slot.allocate_token(token)
            return True
        else:
            # Add to waiting queue
            heapq.heappush(self.waiting_queue, (-token.priority, token))
            return False

    def cancel_token(self, token_id: str) -> bool:
        # Find and cancel the token
        for doctor in self.doctors:
            for slot in doctor.slots:
                if slot.cancel_token(token_id):
                    # Reallocate from waiting queue
                    self.reallocate()
                    return True
        return False

    def reallocate(self):
        # Reallocate waiting tokens to available slots
        while self.waiting_queue:
            priority, token = heapq.heappop(self.waiting_queue)
            if not self.allocate_token(token):
                # Put back if no slot available
                heapq.heappush(self.waiting_queue, (priority, token))
                break

    def add_emergency(self, token: Token):
        # Add emergency with high priority (assume priority 10)
        token.priority = 10
        self.allocate_token(token)

    def get_status(self):
        status = {}
        for doctor in self.doctors:
            status[doctor.id] = {
                'name': doctor.name,
                'slots': [
                    {
                        'time': f"{slot.start_time}-{slot.end_time}",
                        'capacity': f"{slot.current_capacity}/{slot.max_capacity}",
                        'tokens': [str(t) for t in slot.allocated_tokens if t.status == TokenStatus.ALLOCATED]
                    } for slot in doctor.slots
                ]
            }
        return status
