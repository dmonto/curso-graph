import requests
from dotenv import load_dotenv
from B2_6_obtener_token_app_only import obtener_token_app_only

def verificar_licencia_usuario(user_id, token):
    """
    Obtiene licencias del usuario
    
    VENTAJA: Saber qué puede hacer el usuario
    """
    
    headers = {"Authorization": f"Bearer {token}"}
    base_url = "https://graph.microsoft.com/v1.0"
    
    # Obtener licencias asignadas
    response = requests.get(
        f"{base_url}/users/{user_id}/licenseDetails",
        headers=headers
    )
    
    if response.status_code == 200:
        licencias = response.json()["value"]
        
        print(f"📋 LICENCIAS DEL USUARIO: {user_id}\n")
        
        for lic in licencias:
            sku_id = lic.get("skuId")
            sku_name = lic.get("skuPartNumber", "Unknown")
            
            print(f"  • {sku_name} (ID: {sku_id})")
        
        # Determinar nivel
        sku_names = [lic.get("skuPartNumber", "").upper() for lic in licencias]
        
        if "E5" in str(sku_names):
            nivel = "🔴 E5 - PREMIUM (Acceso total)"
        elif "E3" in str(sku_names):
            nivel = "🟡 E3 - ESTÁNDAR (Acceso normal)"
        elif "E1" in str(sku_names):
            nivel = "🟢 E1 - BÁSICO (Acceso limitado)"
        else:
            nivel = "⚠️  ESPECIAL (Verificar manualmente)"
        
        print(f"\n  Nivel: {nivel}")
        
        return {
            "user_id": user_id,
            "licencias": [lic.get("skuPartNumber") for lic in licencias],
            "count": len(licencias)
        }
    else:
        print(f"❌ Error: {response.status_code}")
        return None

# USO (pseudocódigo):
token = obtener_token_app_only()
verificar_licencia_usuario("user@company.com", token)