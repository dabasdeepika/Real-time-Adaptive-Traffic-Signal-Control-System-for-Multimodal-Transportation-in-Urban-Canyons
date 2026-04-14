from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import threading
from routes.traffic_routes import traffic_bp
from routes.ambulance_routes import ambulance_bp
from utils.traffic_simulator import TrafficSimulator

app = Flask(__name__, template_folder='../frontend/templates')
app.config['SECRET_KEY'] = 'trafficiq2024'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

app.register_blueprint(traffic_bp, url_prefix='/api/traffic')
app.register_blueprint(ambulance_bp, url_prefix='/api/ambulance')

simulator = TrafficSimulator(socketio)

@app.route('/')
def index():
    return render_template('dashboard.html')

@socketio.on('connect')
def on_connect():
    emit('connected', {'msg': 'Connected'})

@socketio.on('request_update')
def on_request():
    emit('traffic_update', simulator.get_state())

if __name__ == '__main__':
    t = threading.Thread(target=simulator.run, daemon=True)
    t.start()
    print("TrafficIQ running → http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
