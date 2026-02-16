print("🚀 Starting Trichy Traffic AI...")
from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3, json, os, random
from datetime import datetime

PORT = int(os.environ.get('PORT', 8000))
HOST = '0.0.0.0'

# Auto-create database
conn = sqlite3.connect('data.db')
conn.execute('CREATE TABLE IF NOT EXISTS traffic (loc TEXT, cars INT, weather TEXT, status TEXT)')
conn.commit()
conn.close()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''
<h1>🚗 Trichy Traffic AI - LIVE</h1>
<div id="data">Loading...</div>
<script>
setInterval(()=>fetch("/api").then(r=>r.json()).then(d=>{
document.getElementById("data").innerHTML=`<h2>Predictions</h2><p>${d.pred[0].risk}% risk</p><h2>Traffic</h2><p>${d.traffic[0].loc}: ${d.traffic[0].cars} cars</p>`
}),5000)
</script>'''
            self.wfile.write(html.encode())
        elif self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = {
                "pred": [{"risk": random.randint(20,80)}],
                "traffic": [{"loc": "Chennai Hwy", "cars": random.randint(50,300)}]
            }
            self.wfile.write(json.dumps(data).encode())

print(f"🌐 http://{HOST}:{PORT}")
server = HTTPServer((HOST, PORT), Handler)
server.serve_forever()
