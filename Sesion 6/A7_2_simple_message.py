import requests
import json

# URL del webhook (obtenida al crear el connector)
webhook_url = "https://outlook.webhook.office.com/webhookb2/XXX/IncomingWebhook/XXX"

# Mensaje simple (JSON)
message = {
    "text": "✓ Process completed successfully!"
}

# Enviar
response = requests.post(webhook_url, json=message)
print(f"Status: {response.status_code}")