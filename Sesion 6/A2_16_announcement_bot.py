class AnnouncementBot:
    """Bot que publica anuncios en canales."""
    
    def __init__(self, access_token, team_id):
        self.access_token = access_token
        self.team_id = team_id
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def create_announcements_channel(self):
        """Crea canal de anuncios."""
        payload = {
            "displayName": "Anuncios",
            "description": "Canal para anuncios oficiales",
            "membershipType": "standard"
        }
        
        response = requests.post() # COMPLETAR
        
        if response.status_code == 201:
            return response.json()["id"]
        return None
    
    def publish_announcement(self, channel_id, title, content, priority="normal"):
        """Publica un anuncio formateado."""
        
        color = "#FF0000" if priority == "urgent" else "#0078D4"
        html_content = f"""
        <div style="border-left: 4px solid {color}; padding: 10px; background: #f0f0f0;">
            <h2 style="margin-top: 0; color: {color};">{title}</h2>
            <p>{content}</p>
            <small>Publicado el {datetime.now().strftime('%d/%m/%Y %H:%M')}</small>
        </div>
        """
        
        payload = {
            "body": {
                "contentType": "html",
                "content": html_content
            }
        }
        
        response = requests.post( )  # COMPLETAR
        
        return response.status_code == 201
    
    def get_channel_stats(self, channel_id):
        """Obtiene estadísticas del canal."""
        
        response = requests.get( ) # COMPLETAR
        
        if response.status_code == 200:
            messages = response.json().get("value", [])
            return {
                "total_messages": len(messages),
                "unique_authors": len(set(m.get("from", {}).get("user", {}).get("id") for m in messages)),
                "last_message": messages[0].get("createdDateTime") if messages else None
            }
        
        return None

# USO
bot = AnnouncementBot(access_token, team_id)

# Crear canal
channel_id = bot.create_announcements_channel()

# Publicar anuncios
bot.publish_announcement(
    channel_id,
    "Actualización Importante",
    "Se ha completado la migración del sistema. Por favor, reinicia tu aplicación.",
    priority="urgent"
)

# Ver estadísticas
stats = bot.get_channel_stats(channel_id)
print(f"Mensajes totales: {stats['total_messages']}")
print(f"Autores únicos: {stats['unique_authors']}")