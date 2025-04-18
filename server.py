from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from traffic_simulation import simulate_traffic
import os

app = Flask(__name__)
CORS(app)  # CORS desteği ekle

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/simulation')
def simulation():
    return render_template('simulation.html')

@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    data = request.json
    road_type = data.get('road_type', 'Şehir İçi')
    vehicle_type = data.get('vehicle_type', 'Otomobil')
    speed_limit = data.get('speed_limit', 50)
    
    results = simulate_traffic(road_type, vehicle_type, speed_limit)
    return jsonify(results)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 