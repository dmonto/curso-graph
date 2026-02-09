import os
import requests
from urllib.parse import urlparse, parse_qs
from msal import PublicClientApplication

CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")  
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = "http://localhost"
SCOPES = ["User.Read", "Mail.Read"]  # Delegated + Mail

app = PublicClientApplication(
    client_id=CLIENT_ID,
    authority=AUTHORITY,
)

def get_auth_url():
    """Paso 1: Inicia flow, guarda state, imprime URL"""
    flow = app.initiate_auth_code_flow(scopes=SCOPES, redirect_uri=REDIRECT_URI)
    if "auth_uri" in flow:
        print(f"PASO 1: Abre esta URL en navegador:")
        print(flow["auth_uri"])
        print("\nPASO 2: Después de login/consent, copia la URL COMPLETA de redirect (http://localhost?...):")
        return flow
    raise ValueError(f"Error iniciando flow: {flow}")

def exchange_code_for_token(flow, auth_response_url):
    """Paso 2: Parsea response y exchange (FIX: convierte listas a strings)"""
    parsed = urlparse(auth_response_url)
    if parsed.scheme != "http" or parsed.netloc != "localhost":
        raise ValueError("URL debe ser http://localhost?...")
    
    query_params = parse_qs(parsed.query)
    
    # Convierte TODAS listas a strings (state mismatch killer)
    query_dict = {k: v[0] if isinstance(v, list) and len(v) == 1 else v 
                  for k, v in query_params.items()}
    
    print("Params parseados:", query_dict)  
    
    result = app.acquire_token_by_auth_code_flow(flow, query_dict)
    
    if "access_token" in result:
        print("✅ Token obtenido!")
        return result["access_token"]
    else:
        raise RuntimeError(f"❌ Error: {result.get('error_description', result)}")

def call_graph(token):
    """Paso 3: Llama Graph con token"""
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/mailFolders",
        headers=headers,
        timeout=15
    )
    if resp.status_code == 200:
        print("📧 Mail Folders:", resp.json())
    else:
        print(f"❌ Graph Error {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    print("🔐 MSAL Public Client - Authorization Code Flow CLI")
    flow = get_auth_url()
       
    auth_response = input("\n📋 Pega URL redirect: ").strip()
    token = exchange_code_for_token(flow, auth_response)
    call_graph(token)
    
    print("\n🎉 ¡Funciona! Token válido 1h. Refresh auto en próximas llamadas.")
