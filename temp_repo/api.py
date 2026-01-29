from flask import Flask, request, jsonify
from allocation_engine import AllocationEngine
from models import Doctor, Slot, Token, TokenSource, TokenStatus
from datetime import time

app = Flask(__name__)

# Initialize doctors and engine
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

@app.route('/allocate', methods=['POST'])
def allocate():
    data = request.json
    token = Token(data['id'], data['patient_name'], TokenSource[data['source']], data['priority'])
    success = engine.allocate_token(token)
    return jsonify({'success': success, 'token': str(token)})

@app.route('/cancel/<token_id>', methods=['DELETE'])
def cancel(token_id):
    success = engine.cancel_token(token_id)
    return jsonify({'success': success})

@app.route('/emergency', methods=['POST'])
def emergency():
    data = request.json
    token = Token(data['id'], data['patient_name'], TokenSource.WALK_IN, 10)
    engine.add_emergency(token)
    return jsonify({'success': True, 'token': str(token)})

@app.route('/status', methods=['GET'])
def status():
    return jsonify(engine.get_status())

def run_api():
    app.run(debug=True)

if __name__ == "__main__":
    run_api()
