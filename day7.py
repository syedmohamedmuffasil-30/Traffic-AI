import sqlite3
import random
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

PORT = int(os.environ.get('PORT', 8000))
HOST = os.environ.get('HOST', '0.0.0.0')  # Railway needs 0.0.0.0!

class TrafficDashboard(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = """
<!DOCTYPE html>
<html>
<head>
    <title>🚗 Trichy Traffic AI - Live Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .container { max-width: 1200px; margin: auto; }
        h1 { text-align: center; font-size: 2.5em; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .status { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; margin: 20px 0; backdrop-filter: blur(10px); }
        .prediction { background: linear-gradient(45deg, #ff6b6b, #feca57); padding: 15px; border-radius: 10px; margin: 10px 0; cursor: pointer; transition: transform 0.3s; }
        .prediction:hover { transform: scale(1.02); }
        .live-badge { color: #00ff88; font-weight: bold; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; background: rgba(255,255,255,0.1); border-radius: 10px; overflow: hidden; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.2); }
        th { background: rgba(255,255,255,0.2); }
        .risk-high { background: #ff4444; }
        .risk-medium { background: #ffaa00; }
        .risk-low { background: #44ff44; }
        @media (max-width: 768px) { body { margin: 20px; } h1 { font-size: 2em; } }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚗 Trichy Traffic AI Dashboard <span class="live-badge">🔴 LIVE</span></h1>
        <div class="status">
            <h2>📊 Last Update: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """ IST</h2>
            <p>Auto-refreshes every 30 seconds! 🌐</p>
        </div>
        
        <div id="predictions">
            <h2>🤖 ML Predictions (30 mins ahead)</h2>
            <!-- Predictions populated by JS -->
        </div>
        
        <div id="traffic">
            <h2>🚦 Live Traffic Data</h2>
            <!-- Traffic table populated by JS -->
        </div>
    </div>

    <script>
        function updateDashboard() {
            fetch('/data')
                .then(response => response.json())
                .then(data => {
                    // Update predictions
                    let predsHtml = '';
                    data.predictions.forEach(pred => {
                        let riskClass = pred.risk > 70 ? 'risk-high' : pred.risk > 40 ? 'risk-medium' : 'risk-low';
                        predsHtml += `<div class="prediction ${riskClass}">${pred.location}: <strong>${pred.risk}%</strong> crash risk</div>`;
                    });
                    document.getElementById('predictions').innerHTML = '<h2>🤖 ML Predictions (30 mins ahead)</h2>' + predsHtml;
                    
                    // Update traffic table
                    let tableHtml = '<table><tr><th>Location</th><th>Cars/Hour</th><th>Weather</th><th>Status</th></tr>';
                    data.traffic.forEach(row => {
                        tableHtml += `<tr><td>${row.location}</td><td>${row.cars}</td><td>${row.weather}</td><td>${row.status}</td></tr>`;
                    });
                    tableHtml += '</table>';
                    document.getElementById('traffic').innerHTML = '<h2>🚦 Live Traffic Data</h2>' + tableHtml;
                });
        }
        
        // Update every 30 seconds
        updateDashboard();
        setInterval(updateDashboard, 30000);
    </script>
</body>
</html>
            """
            self.wfile.write(html.encode())
        elif self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Connect to SQLite
            conn = sqlite3.connect('traffic_data.db')
            cursor = conn.cursor()
            
            # Get traffic data
            cursor.execute("SELECT location, cars_per_hour, weather_condition, status FROM traffic_pro ORDER BY timestamp DESC LIMIT 10")
            traffic = [{'location': row[0], 'cars': row[1], 'weather': row[2], 'status': row[3]} for row in cursor.fetchall()]
            
            # ML Predictions (simple neural net simulation)
            predictions = [
                {'location': 'Chennai_Hwy_Junction', 'risk': 37.0},
                {'location': 'Dindigul_Road', 'risk': 22.5},
                {'location': 'Erode_Bypass', 'risk': 45.8},
                {'location': 'Namakkal_Hwy', 'risk': 18.2},
                {'location': 'Karur_Road', 'risk': 61.3},
                {'location': 'Perundurai_Industrial', 'risk': 75.0}
            ]
            
            data = {'traffic': traffic, 'predictions': predictions}
            self.wfile.write(json.dumps(data).encode())
            conn.close()
        else:
            self.send_response(404)
            self.end_headers()

print("🚀 Trichy Traffic AI Dashboard starting...")
print(f"🌐 HOST: {HOST}, PORT: {PORT}")
print("📱 Auto-refreshes every 30s!")

server = HTTPServer((HOST, PORT), TrafficDashboard)
server.serve_forever()

