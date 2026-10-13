import requests
import json

match_id = "5970131"  # Ninte ID

# ✅ CORRECT URL - ithaan fix!
url = f"https://www.fotmob.com/api/data/matchDetails?matchId={match_id}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
}

print(f"Connecting to FotMob server...")
print(f"Fetching Match ID: {match_id}...")

try:
    res = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {res.status_code}")
    
    if res.status_code == 200:
        data = res.json()
        with open(f'al_ahli_{match_id}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"✅ SAVED! al_ahli_{match_id}.json")
        print(f"Shots: {len(data.get('content', {}).get('shotmap', {}).get('shots', []))}")
    else:
        print(f"❌ Error {res.status_code}: {res.text[:200]}")

except Exception as e:
    print(f"❌ Connection Error: {e}")
    print("Tip: WiFi check cheyyu, VPN off aakku!")