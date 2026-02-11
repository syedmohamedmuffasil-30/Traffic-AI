import sqlite3
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime

class TrafficDashboard(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve dashboard HTML
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
<!DOCTYPE html>
<html>
<head>
    <title>🚗 Trichy Traffic AI - Live Dashboard</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #1a1a2e; color: white; }
        .header { text-align: center; font-size: 28px; margin-bottom: 30px; }
        .danger { color: #ff4757; }
        .warning { color: #ffa502; }
        .safe { color: #2ed573; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #333; }
        th { background: #16213e; }
        .status { font-weight: bold; padding: 8px 15px; border-radius: 20px; }
        .ml-prediction { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">🚨 <span style="color: #ff6b6b;">TRICHY TRAFFIC AI</span> - Live Dashboard</div>
    
    <div id="live-data">Loading live Trichy traffic...</div>
    <div id="ml-predictions"></div>
    
    <script>
        function updateDashboard() {
            fetch('/api/traffic')
                .then(r => r.json())
                .then(data => {
                    let html = '<table><tr><th>Road</th><th>Cars/Hour</th><th>Risk</th><th>Weather</th><th>Status</th></tr>';
                    data.forEach(row => {
                        let statusClass = row.alert.includes('CRITICAL') ? 'danger' : 
                                        row.alert.includes('WARNING') ? 'warning' : 'safe';
                        html += `<tr>
                            <td><b>${row.junction}</b></td>
                            <td>${row.cars}</td>
                            <td>${(row.risk*100).toFixed(1)}%</td>
                            <td>${row.weather}</td>
                            <td><span class="status ${statusClass}">${row.alert}</span></td>
                        </tr>`;
                    });
                    html += '</table>';
                    document.getElementById('live-data').innerHTML = html;
                });
            
            fetch('/api/ml')
                .then(r => r.json())
                .then(data => {
                    let html = '<div class="ml-prediction"><h3>🧠 ML PREDICTIONS (30 mins ahead)</h3>';
                    data.forEach(pred => {
                        html += `<p>${pred.junction}: <b>${(pred.risk*100).toFixed(1)}% </b>crash risk</p>`;
                    });
                    html += '</div>';
                    document.getElementById('ml-predictions').innerHTML = html;
                });
        }
        
        updateDashboard();
        setInterval(updateDashboard, 30000);  // Update every 30s
    </script>
</body>
</html>
            """
            self.wfile.write(html.encode())
        
        elif self.path == '/api/traffic':
            self.send_json(self.get_live_traffic())
        
        elif self.path == '/api/ml':
            self.send_json(self.get_ml_predictions())
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def get_live_traffic(self):
        conn = sqlite3.connect('traffic_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT junction, cars, risk, weather, alert FROM traffic_pro ORDER BY risk DESC")
        data = [{"junction": r[0], "cars": r[1], "risk": r[2], "weather": r[3], "alert": r[4]} 
                for r in cursor.fetchall()]
        conn.close()
        return data
    
    def get_ml_predictions(self):
        # Simulate ML predictions
        junctions = ["Chennai_Hwy_Junction", "Dindigul_Road", "Thuvakudi_Industrial"]
        predictions = [{"junction": j, "risk": round(random.uniform(0.2, 0.8), 2)} 
                      for j in junctions]
        return predictions

# 🚀 START YOUR LIVE DASHBOARD!
print("🌐 Starting Trichy Traffic AI Dashboard...")
print("📱 Open: http://localhost:8000")
print("✅ Live updates every 30 seconds!")
print("🎉 Ctrl+C to stop")

server = HTTPServer(('localhost', 8000), TrafficDashboard)
server.serve_forever()
