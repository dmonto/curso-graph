import os

CLIENT_ID_DELEGATED = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Debe coincidir con la URI registrada en la App Registration
REDIRECT_URI = "https://localhost:5001/auth/callback"

SCOPES = ["User.Read"]