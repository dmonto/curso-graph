import requests
from A0_1_get_token import get_delegated_token

SCOPES = ["Mail.ReadWrite"]
token = get_delegated_token(SCOPES)

def get_emails_to_convert(access_token, keywords=None, importance="high"):
    """Obtiene correos que deben convertirse en tareas."""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Construir filtro
    filters = ["isRead eq false"]  # Correos sin leer
    
    if keywords:
        keyword_filters = " or ".join([f"startsWith(subject, '{kw}')" for kw in keywords])
        filters.append(f"({keyword_filters})")
    
    if importance:
        filters.append(f"importance eq '{importance}'")
    
    filter_query = " and ".join(filters)
    
    params = {
        "$filter": filter_query,
        "$select": "id,subject,from,bodyPreview,importance,receivedDateTime,hasAttachments",
        "$orderby": "receivedDateTime desc",
        "$top": 10
    }
    
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages",
        headers=headers,
        params=params
    )
    
    return response.json().get("value", []) if response.status_code == 200 else []

# Uso
keywords = ["Acción requerida", "URGENTE", "TODO"]
emails = get_emails_to_convert(token, keywords=keywords)
print(f"Encontrados {len(emails)} correos para convertir")