import sqlite3
import json
import random
from datetime import datetime

print("🌐 LIVE TRICHY TRAFFIC SCANNER!")
print("=" * 60)

# Connect YOUR database
conn = sqlite3.connect('traffic_database.db')
cursor = conn.cursor()

# 🧹 Clean old data
cursor.execute("DELETE FROM traffic_data")
print("🧹 Database ready for live data!")

# 🚗 SIMULATE LIVE TRAFFIC (Day 5 = Real APIs!)
live_traffic = [
    {"junction": "Dindigul_Road", "cars_per_hour": random.randint(1000, 2000), "accident_risk": round(random.uniform(0.05, 0.25), 2)},
    {"junction": "Chennai_Hwy_Junction", "cars_per_hour": random.randint(1500, 3000), "accident_risk": round(random.uniform(0.3, 0.65), 2)},
    {"junction": "Thuvakudi_Industrial", "cars_per_hour": random.randint(500, 1200), "accident_risk": round(random.uniform(0.02, 0.15), 2)}
]

# 💾 Save LIVE data
for data in live_traffic:
    cursor.execute('''
    INSERT INTO traffic_data (junction, cars_per_hour, accident_risk, recorded_at)
    VALUES (?, ?, ?, ?)
    ''', (data['junction'], data['cars_per_hour'], data['accident_risk'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
conn.commit()
print("✅ LIVE traffic saved!")

# 🤖 AI ANALYSIS
print("\n📊 LIVE TRAFFIC STATUS:")
cursor.execute("SELECT * FROM traffic_data ORDER BY accident_risk DESC")
live_data = cursor.fetchall()
for row in live_data:
    print(f"🚨 {row[0]}: {row[1]} cars | RISK: {row[2]*100:.1f}% | {row[3]}")

print("\n🚨 EMERGENCY ALERTS:")
cursor.execute("SELECT junction FROM traffic_data WHERE accident_risk > 0.3")
danger_zones = cursor.fetchall()
if danger_zones:
    print("ALERT:", ", ".join([zone[0] for zone in danger_zones]))
else:
    print("✅ All roads SAFE!")

conn.close()
print("🎉 LIVE TRAFFIC SYSTEM READY!")
