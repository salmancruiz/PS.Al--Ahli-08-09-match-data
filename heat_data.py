import json
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np

# Load
with open('heatmap_5970131.json', 'r') as f:
    hm = json.load(f)

players_data = hm.get('players', {})

# Dict -> list
if isinstance(players_data, dict):
    players_list = []
    for pid, pdata in players_data.items():
        if isinstance(pdata, list):
            players_list.append({'playerId': pid, 'heatmap': pdata})
        elif isinstance(pdata, dict):
            pts = pdata.get('heatmap') or pdata.get('data') or []
            players_list.append({'playerId': pid, 'heatmap': pts})
else:
    players_list = players_data

print(f"Total: {len(players_list)}")

# Load match for Ahli
with open('al_ahli_5970131.json', 'r', encoding='utf-8') as f:
    match = json.load(f)

lineup_obj = match.get('content',{}).get('lineup',{})
teams = lineup_obj.get('lineup') or lineup_obj.get('teams') or []
ahli_ids = []
for t in teams:
    if 'ahli' in t.get('teamName','').lower():
        ahli_ids = [str(p.get('playerId')) for p in t.get('players',[])]
        break

print(f"Ahli: {ahli_ids[:3]}")

xs=[]; ys=[]
for p in players_list:
    pid=str(p.get('playerId',''))
    if pid in ahli_ids:
        for pt in p.get('heatmap',[]):
            if isinstance(pt, dict):
                x=pt.get('x',0); y=pt.get('y',0)
            else:
                if len(pt)<2: continue
                x=pt[0]; y=pt[1]
            # NO SCALING FIRST - check raw
            xs.append(float(x)); ys.append(float(y))

print(f"Raw xs sample: {xs[:5]}")
print(f"Raw ys sample: {ys[:5]}")
print(f"Points: {len(xs)}")

# Fallback - if empty, take first 15 (Ahli home team)
if len(xs) < 100:
    xs=[]; ys=[]
    for p in players_list[:15]:
        for pt in p.get('heatmap',[])[:300]:
            if isinstance(pt, dict): x=pt.get('x',0); y=pt.get('y',0)
            else:
                if len(pt)<2: continue
                x=pt[0]; y=pt[1]
            xs.append(float(x)); ys.append(float(y))
    print(f"Fallback points: {len(xs)}")

# AUTO SCALE DETECT
# If xs max <=1.5 -> 0-1 range -> scale to 120,80
# If xs max <=100 -> 0-100 range -> scale to 120,80
max_x = max(xs) if xs else 0
print(f"Max X: {max_x}")

if max_x <= 1.5:
    xs = [x*120 for x in xs]
    ys = [y*80 for y in ys]
elif max_x <= 100:
    xs = [x*1.2 for x in xs]
    ys = [y*0.8 for y in ys]

# PLOT - GREEN PITCH + RED HEAT + DOTS - INI KANUM!
pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white', line_zorder=2)
fig, ax = pitch.draw(figsize=(10,7))

# 1. Scatter dots - always visible
pitch.scatter(xs, ys, c='red', s=2, alpha=0.3, ax=ax, zorder=1)

# 2. Heat
pitch.kdeplot(xs, ys, ax=ax, cmap='Reds', fill=True, levels=50, alpha=0.8, bw_adjust=0.6, zorder=3)

plt.title('AL AHLI - ONLY AHLI - FINAL REAL HEAT', fontsize=14, fontweight='bold')
plt.savefig('AL_AHLI_FINAL_RED.png', dpi=300, bbox_inches='tight')
print("✅✅✅ SAVED AL_AHLI_FINAL_RED.png - INI RED VARUM MONE!")
plt.show()