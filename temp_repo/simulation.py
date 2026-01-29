import random
from datetime import datetime, time
from allocation_engine import AllocationEngine
from models import Doctor, Slot, Token, TokenSource, TokenStatus

def simulate_opd_day():
    # Initialize doctors
    doctors = [
        Doctor("D1", "Dr. Smith", [
            Slot("D1", time(9,0), time(10,0), 5),
            Slot("D1", time(10,0), time(11,0), 5),
            Slot("D1", time(11,0), time(12,0), 5),
        ]),
        Doctor("D2", "Dr. Johnson", [
            Slot("D2", time(9,0), time(10,0), 5),
            Slot("D2", time(10,0), time(11,0), 5),
            Slot("D2", time(11,0), time(12,0), 5),
        ]),
        Doctor("D3", "Dr. Williams", [
            Slot("D3", time(9,0), time(10,0), 5),
            Slot("D3", time(10,0), time(11,0), 5),
            Slot("D3", time(11,0), time(12,0), 5),
        ]),
    ]
    engine = AllocationEngine(doctors)

    # Simulate tokens
    token_id = 1
    for hour in range(9, 12):
        for _ in range(random.randint(10, 20)):  # Random arrivals
            source = random.choice(list(TokenSource))
            priority = 1 if source != TokenSource.PAID_PRIORITY else 5
            token = Token(f"T{token_id}", f"Patient {token_id}", source, priority)
            engine.allocate_token(token)
            token_id += 1

        # Simulate cancellations
        for doctor in doctors:
            for slot in doctor.slots:
                if slot.allocated_tokens:
                    if random.random() < 0.1:  # 10% chance
                        token = random.choice(slot.allocated_tokens)
                        engine.cancel_token(token.id)

        # Simulate emergencies
        if random.random() < 0.05:  # 5% chance per hour
            token = Token(f"E{token_id}", f"Emergency {token_id}", TokenSource.WALK_IN, 10)
            engine.add_emergency(token)
            token_id += 1

    # Print final status
    print("Simulation Complete. Final Status:")
    status = engine.get_status()
    for doc_id, doc_status in status.items():
        print(f"Doctor: {doc_status['name']}")
        for slot in doc_status['slots']:
            print(f"  Slot {slot['time']}: {slot['capacity']} tokens: {slot['tokens']}")

if __name__ == "__main__":
    simulate_opd_day()
