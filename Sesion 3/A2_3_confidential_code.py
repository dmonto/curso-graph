import os
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
import requests

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")  
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/Mail.Read"]  # Delegados para Graph
REDIRECT_URI = "http://localhost:5000/getAToken"  # Debe coincidir con app registration

app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY,
    redirect_uri=REDIRECT_URI
)

def get_auth_url():
    """Paso 1: Genera URL para redirigir al usuario (login/consentimiento)"""
    flow = app.initiate_auth_code_flow(scopes=SCOPES)
    if "auth_uri" in flow:
        print(f"1. Ve al usuario a: {flow['auth_uri']}")
        print(f"2. Copia el query string completo de la redirect URI después del login")
        return flow
    raise ValueError("Error iniciando flow")

def exchange_code_for_token(flow, auth_response_url):
    """Paso 2: Intercambia el code por token (backend recibe la redirect)"""
    # Parsea la respuesta de redirect: ?code=ABC&state=XYZ...
    query_params = parse_qs(urlparse(auth_response_url).query)
    result = app.acquire_token_by_auth_code_flow(flow, query_params)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        raise RuntimeError(result.get("error_description", "Error desconocido"))

def call_graph(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/mailFolders",
        headers=headers,
        timeout=15
    )
    resp.raise_for_status()
    print(resp.json())

# Uso (simulado para script; en web app, sería en rutas Flask/FastAPI)
if __name__ == "__main__":
    flow = get_auth_url()
    # SIMULA: Usuario va a auth_uri, loguea, pega aquí la URL completa de redirect
    auth_response = input("Pega la URL de redirect después de login: ").strip()
    token = exchange_code_for_token(flow, auth_response)
    call_graph(token)