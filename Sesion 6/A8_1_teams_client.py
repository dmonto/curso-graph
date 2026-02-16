import requests
import time
import math
from functools import wraps

class TeamsGraphClient:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.rate_limits = {
            'messages_per_channel': {'count': 0, 'window': 60}  # 1 RPS = 60 RPM
        }
    
    def anti_throttle(self, resource_type="general", max_rps=1):
        """
        Decorador que respeta límites específicos de Teams.
        """
        def decorator(func):
            @wraps(func)
            def wrapper(channel_id=None, *args, **kwargs):
                if channel_id and resource_type == "messages_per_channel":
                    # Reset contador si pasó la ventana de 60s
                    if time.time() - self.rate_limits[resource_type]['window'] > 60:
                        self.rate_limits[resource_type]['count'] = 0
                
                # Delay preventivo (1/max_rps segundos)
                sleep_time = 1.0 / max_rps
                time.sleep(sleep_time)
                
                response = func(channel_id, *args, **kwargs)
                
                # Manejar 429 específico de Teams
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 10))
                    print(f"⏳ Throttling Teams. Esperando {retry_after}s...")
                    time.sleep(retry_after)
                    self.rate_limits[resource_type]['count'] += 1
                    return wrapper(channel_id, *args, **kwargs)  # Reintento
                
                return response
            return wrapper
        return decorator
    
    @anti_throttle(resource_type="messages_per_channel", max_rps=0.8)  # 80% del límite
    def post_channel_message(self, team_id, channel_id, message):
        """Envia mensaje respetando 1 RPS por canal."""
        url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages"
        payload = {
            "body": {
                "contentType": "html",
                "content": f"<p>{message}</p>"
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        return response

# --- USO ---
client = TeamsGraphClient("TU_TOKEN")

# Esto enviará mensajes con 1.25s de delay entre cada uno (seguro para 1 RPS)
response = client.post_channel_message(
    team_id="tu-team-id",
    channel_id="tu-channel-id",
    message="✅ Proceso completado automáticamente."
)