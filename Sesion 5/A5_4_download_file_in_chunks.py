import requests
from A0_1_get_token import get_delegated_token

SCOPES = ["Mail.ReadWrite"]
token = get_delegated_token(SCOPES)

def download_file_in_chunks(file_url, output_path, chunk_size=8192):
    """Descarga archivo en chunks para ahorrar memoria."""
    response = requests.get(file_url, stream=True)
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"Descargado: {percent:.1f}%")
    
    print(f"Archivo guardado en {output_path}")

# Uso
download_url = "https://graph.microsoft.com/v1.0/me/messages/123/attachments/456/$value"
download_file_in_chunks(download_url, "archivo_descargado.pdf")