# OPD Token Allocation System

This project implements an Outpatient Department (OPD) token allocation system that manages patient appointments across multiple doctors and time slots. It supports different token sources, priority-based allocation, cancellations, and emergency handling.

## Features

- **Token Allocation**: Allocates patient tokens to available doctor slots based on priority and availability.
- **Priority System**: Supports different priorities (higher number = higher priority) for tokens from various sources (Online, Walk-in, Paid Priority, Follow-up).
- **Cancellation Handling**: Allows cancellation of tokens, which can trigger reallocation from a waiting queue.
- **Emergency Support**: Handles emergency tokens with high priority for immediate allocation.
- **Simulation Mode**: Simulates a full OPD day with random token arrivals, cancellations, and emergencies.
- **REST API**: Provides endpoints for allocating tokens, cancelling tokens, adding emergencies, and checking status.

## Components

### Models (`models.py`)
- `Token`: Represents a patient token with ID, name, source, priority, and status.
- `Slot`: Represents a doctor's time slot with capacity and allocated tokens.
- `Doctor`: Represents a doctor with multiple slots.
- Enums: `TokenSource` and `TokenStatus` for categorization.

### Allocation Engine (`allocation_engine.py`)
- Manages the allocation logic using a priority queue for waiting tokens.
- Finds the earliest available slot for standard tokens.
- Balances load for priority tokens.
- Handles cancellations and reallocations.

### Simulation (`simulation.py`)
- Simulates an OPD day with 3 doctors, each having 3 slots (9-10, 10-11, 11-12).
- Generates random tokens, cancellations, and emergencies.
- Prints the final status of all slots.

### API (`api.py`)
- Flask-based REST API with endpoints:
  - `POST /allocate`: Allocate a new token.
  - `DELETE /cancel/<token_id>`: Cancel a token.
  - `POST /emergency`: Add an emergency token.
  - `GET /status`: Get current status of all doctors and slots.

## Usage

### Running the Simulation
```bash
python main.py
```

This runs the simulation and outputs the final status.

### Running the API
```bash
python main.py api
```

Starts the Flask server on `http://localhost:5000`.

### API Endpoints

#### Allocate Token
```bash
curl -X POST http://localhost:5000/allocate \
  -H "Content-Type: application/json" \
  -d '{"id": "T1", "patient_name": "John Doe", "source": "WALK_IN", "priority": 1}'
```

#### Cancel Token
```bash
curl -X DELETE http://localhost:5000/cancel/T1
```

#### Add Emergency
```bash
curl -X POST http://localhost:5000/emergency \
  -H "Content-Type: application/json" \
  -d '{"id": "E1", "patient_name": "Emergency Patient"}'
```

#### Get Status
```bash
curl http://localhost:5000/status
```

## Sample Output

When running the simulation (`python main.py`), the output shows the final allocation status:

```
Simulation Complete. Final Status:
Doctor: Dr. Smith
  Slot 09:00:00-10:00:00: 5/5 tokens: ['Token(id=T1, patient=Patient 1, source=WALK_IN, priority=1)', 'Token(id=T2, patient=Patient 2, source=ONLINE, priority=1)', 'Token(id=T3, patient=Patient 3, source=WALK_IN, priority=1)', 'Token(id=T4, patient=Patient 4, source=WALK_IN, priority=1)', 'Token(id=T5, patient=Patient 5, source=WALK_IN, priority=1)']
  Slot 10:00:00-11:00:00: 5/5 tokens: ['Token(id=T16, patient=Patient 16, source=FOLLOW_UP, priority=1)', 'Token(id=T17, patient=Patient 17, source=FOLLOW_UP, priority=1)', 'Token(id=T18, patient=Patient 18, source=PAID_PRIORITY, priority=5)', 'Token(id=T19, patient=Patient 19, source=WALK_IN, priority=1)', 'Token(id=T20, patient=Patient 20, source=WALK_IN, priority=1)']
  Slot 11:00:00-12:00:00: 5/5 tokens: ['Token(id=T31, patient=Patient 31, source=PAID_PRIORITY, priority=5)', 'Token(id=T32, patient=Patient 32, source=ONLINE, priority=1)', 'Token(id=T33, patient=Patient 33, source=ONLINE, priority=1)', 'Token(id=T34, patient=Patient 34, source=ONLINE, priority=1)', 'Token(id=T35, patient=Patient 35, source=WALK_IN, priority=1)']
Doctor: Dr. Johnson
  Slot 09:00:00-10:00:00: 5/5 tokens: ['Token(id=T6, patient=Patient 6, source=ONLINE, priority=1)', 'Token(id=T7, patient=Patient 7, source=PAID_PRIORITY, priority=5)', 'Token(id=T8, patient=Patient 8, source=FOLLOW_UP, priority=1)', 'Token(id=T9, patient=Patient 9, source=WALK_IN, priority=1)', 'Token(id=T10, patient=Patient 10, source=WALK_IN, priority=1)']
  Slot 10:00:00-11:00:00: 5/5 tokens: ['Token(id=T22, patient=Patient 22, source=ONLINE, priority=1)', 'Token(id=T23, patient=Patient 23, source=WALK_IN, priority=1)', 'Token(id=T24, patient=Patient 24, source=WALK_IN, priority=1)', 'Token(id=T25, patient=Patient 25, source=ONLINE, priority=1)', 'Token(id=T40, patient=Patient 40, source=WALK_IN, priority=1)']
  Slot 11:00:00-12:00:00: 5/5 tokens: ['Token(id=T36, patient=Patient 36, source=WALK_IN, priority=1)', 'Token(id=T37, patient=Patient 37, source=PAID_PRIORITY, priority=5)', 'Token(id=T38, patient=Patient 38, source=ONLINE, priority=1)', 'Token(id=T39, patient=Patient 39, source=WALK_IN, priority=1)', 'Token(id=T41, patient=Patient 41, source=ONLINE, priority=1)']
Doctor: Dr. Williams
  Slot 09:00:00-10:00:00: 5/5 tokens: ['Token(id=T11, patient=Patient 11, source=ONLINE, priority=1)', 'Token(id=T12, patient=Patient 12, source=FOLLOW_UP, priority=1)', 'Token(id=T13, patient=Patient 13, source=FOLLOW_UP, priority=1)', 'Token(id=T14, patient=Patient 14, source=PAID_PRIORITY, priority=5)', 'Token(id=T15, patient=Patient 15, source=PAID_PRIORITY, priority=5)']
  Slot 10:00:00-11:00:00: 5/5 tokens: ['Token(id=T26, patient=Patient 26, source=PAID_PRIORITY, priority=5)', 'Token(id=T27, patient=Patient 27, source=FOLLOW_UP, priority=1)', 'Token(id=T28, patient=Patient 28, source=PAID_PRIORITY, priority=5)', 'Token(id=T29, patient=Patient 29, source=WALK_IN, priority=1)', 'Token(id=T30, patient=Patient 30, source=WALK_IN, priority=1)']
  Slot 11:00:00-12:00:00: 5/5 tokens: ['Token(id=T42, patient=Patient 42, source=FOLLOW_UP, priority=1)', 'Token(id=T43, patient=Patient 43, source=ONLINE, priority=1)', 'Token(id=T44, patient=Patient 44, source=ONLINE, priority=1)', 'Token(id=T45, patient=Patient 45, source=WALK_IN, priority=1)', 'Token(id=T46, patient=Patient 46, source=FOLLOW_UP, priority=1)']
```

This shows the allocation of tokens across doctors and slots, with each slot showing its capacity usage and list of allocated patients.

## Requirements

- Python 3.6+
- Flask (for API mode)

Install dependencies:
```bash
pip install flask
```

## TODO

- Add logging and monitoring
- Optimize performance for high load
- Add unit tests
