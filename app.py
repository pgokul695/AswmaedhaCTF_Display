from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json
import os
from functools import wraps

app = Flask(__name__)
CORS(app)

# API Key for authentication (in production, use environment variables)
API_KEY = "ctf_admin_2026_ashwamedha"
TIMER_STATE_FILE = "timer_state.json"

# Authentication decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != API_KEY:
            return jsonify({"error": "Unauthorized", "message": "Invalid API key"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Timer state management
def load_timer_state():
    """Load timer state from JSON file"""
    if os.path.exists(TIMER_STATE_FILE):
        with open(TIMER_STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "start_time": None,
        "duration_seconds": 7200,
        "remaining_seconds": 7200,
        "is_running": False,
        "last_updated": None
    }

def save_timer_state(state):
    """Save timer state to JSON file"""
    with open(TIMER_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def calculate_remaining_time(state):
    """Calculate actual remaining time based on start time"""
    if not state["is_running"] or state["start_time"] is None:
        return state["remaining_seconds"]
    
    start_time = datetime.fromisoformat(state["start_time"])
    elapsed = (datetime.now() - start_time).total_seconds()
    remaining = max(0, state["duration_seconds"] - elapsed)
    return int(remaining)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/timer/status', methods=['GET'])
def get_timer_status():
    """Get current timer status (public endpoint)"""
    state = load_timer_state()
    remaining = calculate_remaining_time(state)
    
    return jsonify({
        "is_running": state["is_running"],
        "remaining_seconds": remaining,
        "duration_seconds": state["duration_seconds"],
        "start_time": state["start_time"]
    })

@app.route('/api/timer/start', methods=['POST'])
@require_api_key
def start_timer():
    """Start the 2-hour timer (authenticated)"""
    state = load_timer_state()
    
    if state["is_running"]:
        return jsonify({"error": "Timer already running"}), 400
    
    state["start_time"] = datetime.now().isoformat()
    state["is_running"] = True
    state["last_updated"] = datetime.now().isoformat()
    save_timer_state(state)
    
    return jsonify({
        "message": "Timer started",
        "start_time": state["start_time"],
        "duration_seconds": state["duration_seconds"]
    })

@app.route('/api/timer/sync', methods=['POST'])
@require_api_key
def sync_timer():
    """Sync remaining time from client (authenticated)"""
    state = load_timer_state()
    data = request.get_json()
    
    if not data or 'remaining_seconds' not in data:
        return jsonify({"error": "Missing remaining_seconds"}), 400
    
    # Get server's authoritative time
    server_remaining = calculate_remaining_time(state)
    client_remaining = data['remaining_seconds']
    
    # Allow small drift (5 seconds), but correct large differences
    drift = abs(server_remaining - client_remaining)
    
    if drift > 5:
        # Server time is authoritative, send correction
        return jsonify({
            "message": "Time corrected",
            "server_remaining": server_remaining,
            "client_remaining": client_remaining,
            "drift_seconds": drift,
            "corrected": True
        })
    
    state["last_updated"] = datetime.now().isoformat()
    save_timer_state(state)
    
    return jsonify({
        "message": "Sync successful",
        "server_remaining": server_remaining,
        "corrected": False
    })

@app.route('/api/timer/stop', methods=['POST'])
@require_api_key
def stop_timer():
    """Stop the timer (authenticated)"""
    state = load_timer_state()
    
    if not state["is_running"]:
        return jsonify({"error": "Timer not running"}), 400
    
    # Calculate and save remaining time
    remaining = calculate_remaining_time(state)
    state["remaining_seconds"] = remaining
    state["is_running"] = False
    state["start_time"] = None
    state["last_updated"] = datetime.now().isoformat()
    save_timer_state(state)
    
    return jsonify({
        "message": "Timer stopped",
        "remaining_seconds": remaining
    })

@app.route('/api/timer/reset', methods=['POST'])
@require_api_key
def reset_timer():
    """Reset timer to 2 hours (authenticated)"""
    state = {
        "start_time": None,
        "duration_seconds": 7200,
        "remaining_seconds": 7200,
        "is_running": False,
        "last_updated": datetime.now().isoformat()
    }
    save_timer_state(state)
    
    return jsonify({
        "message": "Timer reset to 2 hours",
        "duration_seconds": 7200
    })

@app.route('/api/timer/set-duration', methods=['POST'])
@require_api_key
def set_duration():
    """Set custom timer duration (authenticated)"""
    data = request.get_json()
    
    if not data or 'duration_minutes' not in data:
        return jsonify({"error": "Missing duration_minutes"}), 400
    
    duration_minutes = data['duration_minutes']
    if duration_minutes < 1 or duration_minutes > 300:
        return jsonify({"error": "Duration must be between 1 and 300 minutes"}), 400
    
    duration_seconds = duration_minutes * 60
    state = load_timer_state()
    
    # Only allow changing duration when timer is stopped
    if state["is_running"]:
        return jsonify({"error": "Stop the timer before changing duration"}), 400
    
    state["duration_seconds"] = duration_seconds
    state["remaining_seconds"] = duration_seconds
    state["last_updated"] = datetime.now().isoformat()
    save_timer_state(state)
    
    return jsonify({
        "message": f"Timer duration set to {duration_minutes} minutes",
        "duration_seconds": duration_seconds
    })

if __name__ == '__main__':
    print("=" * 60)
    print("  CTF Challenge Display - Ashwamedha'26")
    print("=" * 60)
    print("")
    print("Starting Flask server...")
    print("Access at: http://localhost:5000")
    print("From other devices: http://YOUR_IP:5000")
    print("")
    print("API Endpoints:")
    print("  GET  /api/timer/status  - Get timer status (public)")
    print("  POST /api/timer/start   - Start timer (auth required)")
    print("  POST /api/timer/sync    - Sync timer (auth required)")
    print("  POST /api/timer/stop    - Stop timer (auth required)")
    print("  POST /api/timer/reset   - Reset timer (auth required)")
    print("")
    print(f"API Key: {API_KEY}")
    print("")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5009)
