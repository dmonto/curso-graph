from typing import List, Dict
import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Mail.Read"]
token = get_delegated_token(SCOPES)

def get_all_messages_paginated(access_token, top=25):
    """
    Inbox directo SIN folder ID.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    
    all_messages = []
    url = "https://graph.microsoft.com/v1.0/me/messages"  # ← Inbox default
    
    params = {"$top": top, "$select": "subject,from,receivedDateTime"}
    
    while url and len(all_messages) < 1000:  # Límite razonable
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"❌ Error {response.status_code}: {response.text}")
            break
        
        data = response.json()
        all_messages.extend(data.get("value", []))
        
        url = data.get("@odata.nextLink")
        params = {}  # NextLink ya tiene todo
        
        print(f"📥 {len(data['value'])} msgs. Total: {len(all_messages)}")
    
    return all_messages

# Uso
messages = get_all_messages_paginated(token)
print(f"Total de mensajes: {len(messages)}")