import json
import webbrowser
import os
import plotly.graph_objects as go

with open('al_ahli_5970131.json', 'r', encoding='utf-8') as f:
    match_data = json.load(f)

raw_shots = match_data.get("content", {}).get("shotmap", {}).get("shots", [])
al_ahli_id = 9743

goal_x, goal_y, goal_text = [], [], []
miss_x, miss_y, miss_text = [], [], []

for shot in raw_shots:
    if shot.get("teamId") == al_ahli_id:
        x = (float(shot.get("x", 0)) / 100) * 120
        y = (float(shot.get("y", 0)) / 100) * 80
        player = shot.get("playerName", "Al Ahli Player")
        minute = shot.get("min", "0")
        situation = shot.get("situation", "Open Play")
        
        info = f"Player: {player}<br>Minute: {minute}'<br>Situation: {situation}"
        
        if shot.get("eventType") == "Goal":
            goal_x.append(x)
            goal_y.append(y)
            goal_text.append(info)
        else:
            miss_x.append(x)
            miss_y.append(y)
            miss_text.append(info)

fig = go.Figure()

fig.add_shape(type="rect", x0=0, y0=0, x1=120, y1=80, line=dict(color="white", width=2), fillcolor="#1c1c1c")
fig.add_shape(type="rect", x0=102, y0=18, x1=120, y1=62, line=dict(color="white", width=2))
fig.add_shape(type="rect", x0=114, y0=30, x1=120, y1=50, line=dict(color="white", width=2))
fig.add_shape(type="line", x0=60, y0=0, x1=60, y1=80, line=dict(color="white", width=2))
fig.add_shape(type="circle", x0=50, y0=30, x1=70, y1=50, line=dict(color="white", width=2))

fig.add_trace(go.Scatter(
    x=goal_x, y=goal_y, mode='markers', name='Goals',
    marker=dict(size=14, color='#d32f2f', line=dict(width=0)),
    text=goal_text, hoverinfo='text'
))

fig.add_trace(go.Scatter(
    x=miss_x, y=miss_y, mode='markers', name='Shots',
    marker=dict(size=12, color='rgba(0,0,0,0)', line=dict(color='#00e5ff', width=2)),
    text=miss_text, hoverinfo='text'
))

html_content = f"""
<html>
<head>
    <title>Playscope Analytics Dashboard</title>
    <style>
        body {{ background-color: #1c1c1c; color: white; font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        .header {{ margin-bottom: 20px; }}
        .header h1 {{ margin: 0; font-size: 24px; font-weight: bold; }}
        .header p {{ margin: 5px 0 0 0; color: #aaaaaa; font-size: 14px; }}
        .footer {{ margin-top: 30px; display: flex; justify-content: space-between; font-size: 13px; border-top: 1px solid #333; padding-top: 15px; }}
        .footer-left {{ color: #00e5ff; font-weight: bold; line-height: 1.5; }}
        .footer-right a {{ color: #aaaaaa; text-decoration: none; margin-left: 15px; }}
        .footer-right a:hover {{ color: #00e5ff; text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Al Ahli Shots Map</h1>
        <p>Saudi Pro League | Match Analysis Report</p>
    </div>
    
    {fig.to_html(full_html=False, include_plotlyjs='cdn')}
    
    <div class="footer">
        <div class="footer-left">
            POWERED BY PLAYSCOPE Analytics<br>
            Developer: Salman Vasudev
        </div>
        <div class="footer-right">
            <b>Profiles:</b>
            <a href="https://github.com" target="_blank">GitHub</a>
            <a href="https://linkedin.com" target="_blank">LinkedIn</a>
        </div>
    </div>
</body>
</html>
"""

output_html = "playscope_dashboard.html"
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_content)

webbrowser.open('file://' + os.path.realpath(output_html))
print("Web Dashboard generated successfully! Clickable links are ready in your browser.")
