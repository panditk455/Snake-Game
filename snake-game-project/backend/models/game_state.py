import json
import time
from datetime import datetime

class GameState:
    def __init__(self):
        self.sessions = {}
        self.high_scores = []
    
    def create_session(self, session_id, player_name="Anonymous"):
        self.sessions[session_id] = {
            'player_name': player_name,
            'score': 0,
            'start_time': time.time(),
            'status': 'active',
            'snake_length': 2,
            'food_eaten': 0
        }
        return self.sessions[session_id]
    
    def update_session(self, session_id, **kwargs):
        if session_id in self.sessions:
            self.sessions[session_id].update(kwargs)
            return self.sessions[session_id]
        return None
    
    def end_session(self, session_id):
        if session_id in self.sessions:
            session = self.sessions[session_id]
            game_duration = time.time() - session['start_time']
            
            high_score_entry = {
                'player_name': session['player_name'],
                'score': session['score'],
                'timestamp': datetime.now().isoformat(),
                'game_duration': round(game_duration, 2),
                'food_eaten': session.get('food_eaten', 0)
            }
            
            self.high_scores.append(high_score_entry)
            del self.sessions[session_id]
            return high_score_entry
        return None
    
    def get_high_scores(self, limit=10):
        return sorted(self.high_scores, key=lambda x: x['score'], reverse=True)[:limit]
    
    def save_to_file(self, filename='game_data.json'):
        data = {
            'high_scores': self.high_scores,
            'last_updated': datetime.now().isoformat()
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filename='game_data.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.high_scores = data.get('high_scores', [])
        except FileNotFoundError:
            self.high_scores = []

# Global game state instance
game_state = GameState()