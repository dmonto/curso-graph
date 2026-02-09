import requests
from azure.identity import DefaultAzureCredential  # no es MSAL, pero usa Entra por debajo
# pip install azure-identity

GRAPH_SCOPE = "https://graph.microsoft.com/.default"  # resource + .default

def get_token_managed_identity():
    # En Azure Functions, DefaultAzureCredential usará la managed identity por defecto
    cred = DefaultAzureCredential()
    token = cred.get_token(GRAPH_SCOPE)
    return token.token

def run_job():
    token = get_token_managed_identity()
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/users?$top=5&$select=id,displayName,mail",
        headers=headers,
        timeout=15,
    )
    resp.raise_for_status()
    print(resp.json())

run_job()