from backend.app import app, socketio

if __name__ == '__main__':
    print("🐍 Starting Snake Game Server...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)