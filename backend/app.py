from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import time
from datetime import datetime

app = Flask(__name__, 
            template_folder='../frontend',
            static_folder='../frontend/static')
app.config['SECRET_KEY'] = 'snake_game_secret_key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage for game data
game_sessions = {}
high_scores = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/high-scores', methods=['GET'])
def get_high_scores():
    # Return top 10 high scores
    sorted_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)
    return jsonify(sorted_scores[:10])

@app.route('/api/high-scores', methods=['POST'])
def save_high_score():
    data = request.json
    score_entry = {
        'player_name': data.get('player_name', 'Anonymous'),
        'score': data.get('score', 0),
        'timestamp': datetime.now().isoformat(),
        'game_duration': data.get('game_duration', 0)
    }
    high_scores.append(score_entry)
    return jsonify({"message": "Score saved successfully", "entry": score_entry})

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    emit('connected', {'data': 'Connected to Snake Game Server'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')
    if request.sid in game_sessions:
        del game_sessions[request.sid]

@socketio.on('start_game')
def handle_start_game(data):
    session_id = request.sid
    game_sessions[session_id] = {
        'player_name': data.get('player_name', 'Anonymous'),
        'start_time': time.time(),
        'score': 0,
        'status': 'playing'
    }
    emit('game_started', {'session_id': session_id})

@socketio.on('update_score')
def handle_update_score(data):
    session_id = request.sid
    if session_id in game_sessions:
        game_sessions[session_id]['score'] = data.get('score', 0)
        emit('score_updated', {'score': data.get('score', 0)})

@socketio.on('game_over')
def handle_game_over(data):
    session_id = request.sid
    if session_id in game_sessions:
        session = game_sessions[session_id]
        final_score = data.get('score', 0)
        game_duration = time.time() - session['start_time']
        
        # Save to high scores
        score_entry = {
            'player_name': session['player_name'],
            'score': final_score,
            'timestamp': datetime.now().isoformat(),
            'game_duration': round(game_duration, 2)
        }
        high_scores.append(score_entry)
        
        emit('game_ended', {
            'final_score': final_score,
            'game_duration': round(game_duration, 2),
            'high_score_entry': score_entry
        })

if __name__ == '__main__':
    socketio.run(app, debug=True)