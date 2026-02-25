import msal

class GraphAuth:
    def __init__(self, client_id, client_secret, tenant_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.access_token = None
        self.authenticate()
    
    def authenticate(self):
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        
        app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,  
            authority=authority
        )
        
        scopes = ["https://graph.microsoft.com/.default"]
        result = app.acquire_token_for_client(scopes=scopes)
        
        if "access_token" in result:
            self.access_token = result["access_token"]
            return True
        else:
            raise Exception(f"Error autenticando: {result}")
    
    def get_headers(self, renew=False):
        if not self.access_token or renew:
            self.authenticate()
        return {"Authorization": f"Bearer {self.access_token}"}