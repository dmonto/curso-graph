import requests
import os
from A0_1_get_token import get_delegated_token

def send_html_message(access_token, team_id, channel_id, html_content):
    """Publica un mensaje con formato HTML."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "body": {
            "contentType": "html",
            "content": html_content
        }
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json=payload,
        timeout=30
    )
    print(response.json())
    return response.status_code == 201

# USO
SCOPES = ["ChannelMessage.Send"]
token = get_delegated_token(SCOPES)
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
html = """
<h2>Informe de Ventas</h2>
<p>Las ventas del trimestre fueron <strong>excelentes</strong>.</p>
<ul>
  <li>Q1: $100k</li>
  <li>Q2: $120k</li>
  <li>Q3: $150k</li>
</ul>
"""

send_html_message(token, team_id, channel_id, html)