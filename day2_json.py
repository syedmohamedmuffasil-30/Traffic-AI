import json
import os

print("🔍 Checking files...")
print(f"trichy_traffic.json exists? {os.path.exists('trichy_traffic.json')}")

try:
    # 🚗 Read Trichy traffic
    with open('trichy_traffic.json', 'r') as file:
        traffic_data = json.load(file)
    
    print("🚦 TRICHY TRAFFIC SCANNER!")
    print("=" * 40)
    
    for junction in traffic_data:
        name = junction['junction']
        cars = junction['cars_per_hour']
        risk = junction['accident_risk'] * 100
        
        print(f"📍 {name}")
        print(f"   🚗 Cars: {cars}")
        print(f"   ⚠️  Risk: {risk:.0f}%")
        print("-" * 20)
    
    # AI Alert!
    high_risk = [j for j in traffic_data if j['accident_risk'] > 0.3]
    print(f"\n🚨 EMERGENCY: {len(high_risk)} HIGH RISK junctions!")
    
except FileNotFoundError:
    print("❌ ERROR: trichy_traffic.json missing! Create it first.")
except json.JSONDecodeError:
    print("❌ ERROR: JSON broken! Check commas/brackets.")
except Exception as e:
    print(f"❌ Oops: {e}")
