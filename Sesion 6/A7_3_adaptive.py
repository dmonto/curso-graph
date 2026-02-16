import requests
import json

webhook_url = "https://outlook.webhook.office.com/webhookb2/XXX/IncomingWebhook/XXX"

# Adaptive Card
card = {
    "type": "message",
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "contentUrl": None,
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.4",
                "body": [
                    {
                        "type": "Container",
                        "style": "emphasis",
                        "items": [
                            {
                                "type": "ColumnSet",
                                "columns": [
                                    {
                                        "width": "stretch",
                                        "items": [
                                            {
                                                "type": "TextBlock",
                                                "text": "✓ Process Completed",
                                                "weight": "bolder",
                                                "size": "large",
                                                "color": "good"
                                            },
                                            {
                                                "type": "TextBlock",
                                                "text": "Daily data sync finished successfully",
                                                "size": "small",
                                                "isSubtle": True,
                                                "wrap": True
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "Container",
                        "items": [
                            {
                                "type": "FactSet",
                                "facts": [
                                    {
                                        "name": "Process:",
                                        "value": "Daily Data Sync"
                                    },
                                    {
                                        "name": "Duration:",
                                        "value": "5 minutes 23 seconds"
                                    },
                                    {
                                        "name": "Records:",
                                        "value": "10,234 processed"
                                    },
                                    {
                                        "name": "Status:",
                                        "value": "✓ Success"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "actions": [
                    {
                        "type": "Action.OpenUrl",
                        "title": "View Details",
                        "url": "https://dashboard.example.com/logs/12345"
                    },
                    {
                        "type": "Action.OpenUrl",
                        "title": "View Errors",
                        "url": "https://dashboard.example.com/errors/12345"
                    }
                ]
            }
        }
    ]
}

# Enviar
response = requests.post(webhook_url, json=card)
print(f"Status: {response.status_code}")