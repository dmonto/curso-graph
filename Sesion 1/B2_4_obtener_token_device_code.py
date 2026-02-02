from msal import PublicClientApplication

CLIENT_ID = "TU_CLIENT_ID_DELEGATED"
TENANT_ID = "TU_TENANT_ID"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

def obtener_token_device_code():
    app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)

    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise RuntimeError("No se pudo iniciar el device flow")

    print("Ve a la URL siguiente e introduce el código:")
    print(flow["verification_uri"])
    print("Código:", flow["user_code"])

    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError(f"Error en autenticación: {result.get('error_description')}")

    return result["access_token"]