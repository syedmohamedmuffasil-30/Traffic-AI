import sqlite3
import json

print("🗄️  TRICHY TRAFFIC DATABASE - FIXED!")
print("=" * 50)

# 🗄️ 1. Connect database (DO NOT CLOSE YET!)
conn = sqlite3.connect('traffic_database.db')
cursor = conn.cursor()

# 🧹 2. CLEAN old data FIRST (before ANYTHING else)
cursor.execute("DELETE FROM traffic_data")
print("🧹 Database cleaned!")

# 3. Create table (Excel columns)
cursor.execute('''
CREATE TABLE IF NOT EXISTS traffic_data (
    junction TEXT,
    cars_per_hour INTEGER,
    accident_risk REAL,
    recorded_at TEXT
)
''')
print("✅ Table ready!")

# 4. Load YOUR JSON
with open('trichy_traffic.json', 'r') as f:
    traffic_list = json.load(f)

# 5. Save to database (CLEAN data only)
for data in traffic_list:
    cursor.execute('''
    INSERT INTO traffic_data 
    (junction, cars_per_hour, accident_risk, recorded_at)
    VALUES (?, ?, ?, datetime('now'))
    ''', (data['junction'], data['cars_per_hour'], data['accident_risk']))

conn.commit()
print("✅ Fresh traffic saved!")

# 6. ASK QUESTIONS (Database still OPEN!)
print("\n📊 ALL JUNCTIONS:")
cursor.execute("SELECT * FROM traffic_data")
print(cursor.fetchall())

print("\n🚨 DANGEROUS ROADS (>30% risk):")
cursor.execute("SELECT junction, accident_risk FROM traffic_data WHERE accident_risk > 0.3")
danger = cursor.fetchall()
print(danger)

# 🔒 7. NOW close database (LAST STEP ONLY!)
conn.close()
print("🎉 DATABASE WORKS PERFECTLY!")
