# Sesión 5

## Contenidos de Hoy

1. Outlook
2. Descanso
3. Ejercicios
4. Recap y Dudas
5. Cuestionario\\

***

#### `git pull --rebase` en curso-graph

o bien

{% file src="<https://2636242173-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FQqIs3JJP8Yms3lT3YaSM%2Fuploads%2FP5xlgti6TMwL0wLxuTIy%2FSesion%205.zip?alt=media&token=57514a94-92bf-4955-b4d6-cdcf61354af5>" %}

***

## CORREO ELECTRÓNICO Y CALENDARIOS (OUTLOOK)

### Lectura de mensajes: bandeja de entrada, filtros y adjuntos <a href="#microsoft-graph-la-puerta-de-enlace-del-ecosistema" id="microsoft-graph-la-puerta-de-enlace-del-ecosistema"></a>

#### Estructura de carpetas en Outlook/Exchange

En el correo, los mensajes se organizan en **mailFolders** jerárquicamente:

* **Carpetas del sistema**:
  * **`Inbox`** (bandeja de entrada).
  * **`Drafts`** (borradores).
  * **`SentItems`** (elementos enviados).
  * **`DeletedItems`** (papelera).
  * **`ArchiveDeletedItems`** (papelera de archivo).
  * Etc.
* **Carpetas personalizadas**: creadas por el usuario.
* **Estructura**: pueden ser anidadas (subcarpetas de Inbox, p.ej. "Proyectos/2026").​

#### Propiedades clave de un mensaje

<pre class="language-json" data-overflow="wrap" data-expandable="true"><code class="lang-json">{
<strong>  "id": "AAMkADA1M-z...",
</strong><strong>  "subject": "Reunión Mañana",
</strong><strong>  "from": {
</strong>    "emailAddress": {
      "address": "sender@cursograph.onmicrosoft.com",
      "name": "Juan Pérez"
    }
  },
  "toRecipients": [...],
  "ccRecipients": [...],
  "receivedDateTime": "2025-01-09T10:30:00Z",
  "sentDateTime": "2025-01-09T10:25:00Z",
  "isRead": false,
  "hasAttachments": true,
  "bodyPreview": "Hablemos de los resultados de 1T...",
  "body": {
    "contentType": "html|text",
    "content": "..."
  },
  "conversationId": "AAQkADA1M-...",
  "importance": "normal|high|low",
  "categories": ["work", "follow-up"]
}
</code></pre>

**Propiedades importantes**​

* **`isRead`**: booleano, indica si el mensaje ha sido leído.
* **`hasAttachments`**: booleano, indica si hay archivos adjuntos.
* **`receivedDateTime`**: timestamp ISO 8601 de cuándo se recibió.
* **`importance`**: "normal", "high", o "low".

#### Adjuntos

Un mensaje puede tener múltiples adjuntos. Estructura:

{% code overflow="wrap" expandable="true" %}

```json
{
  "id": "AAMkADA1M-CJKtzm...",
  "@odata.type": "#microsoft.graph.fileAttachment",
  "name": "report.pdf",
  "contentType": "application/pdf",
  "size": 2048000,
  "isInline": false,
  "contentId": null
}
```

{% endcode %}

Tipos de adjuntos:​

* **`#microsoft.graph.fileAttachment`**: archivos regulares.
* **`#microsoft.graph.itemAttachment`**: items de Outlook (mensajes, eventos).
* **`#microsoft.graph.referenceAttachment`**: referencias (OneDrive, etc.)

#### 🔗 Endpoints: `/mailFolders`, `/messages`, filtros, adjuntos <a href="#undefined" id="undefined"></a>

#### 1. Listar carpetas

[**GET /me/mailFolders**](https://developer.microsoft.com/graph/graph-explorer?request=me%2FmailFolders\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

[**GET /users/{userId}/mailFolders**](https://developer.microsoft.com/graph/graph-explorer?request=users%2F%7BuserId%7D%2FmailFolders\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)   (una vez en Explorer, inyectar userId)

Devuelve lista de carpetas. Para carpetas del sistema:

[**GET /me/mailFolders/Inbox**](https://developer.microsoft.com/graph/graph-explorer?request=me%2FmailFolders%2FInbox\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

[**GET /me/mailFolders/Drafts**](https://developer.microsoft.com/graph/graph-explorer?request=me%2FmailFolders%2FDrafts\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

O usar IDs de carpeta si son personalizadas.

#### 2. Listar mensajes de una carpeta

[**GET /me/mailFolders/Inbox/messages**](https://developer.microsoft.com/graph/graph-explorer?request=me%2FmailFolders%2FInbox%2Fmessages\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

\
[**GET /me/mailFolders/{folderId}/messages**](https://developer.microsoft.com/graph/graph-explorer?request=me%2FmailFolders%2F%7BfolderId%7D%2Fmessages\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

Con paginación y select:​

[**GET /me/mailFolders/Inbox/messages?$top=10&$select=id,subject,from,isRead,receivedDateTime**](https://developer.microsoft.com/graph/graph-explorer?request=me%2FmailFolders%2FInbox%2Fmessages%3F%24top%3D10%26%24select%3Did%2Csubject%2Cfrom%2CisRead%2CreceivedDateTime\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

#### 3. Filtrar mensajes

Usar `$filter` con operadores lógicos:

**Mensajes no leídos:**

[**GET /me/messages?$filter=isRead eq false**](https://developer.microsoft.com/graph/graph-explorer?request=me%2Fmessages%3F%24filter%3DisRead%2Beq%2Bfalse\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

**Mensajes recibidos después de una fecha:**

[**GET /me/messages?$filter=receivedDateTime gt 2025-01-01T00:00:00Z**](https://developer.microsoft.com/graph/graph-explorer?request=me%2Fmessages%3F%24filter%3DreceivedDateTime%2Bgt%2B2025-01-01T00%3A00%3A00Z\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

**Combinación (and):**

[**GET /me/messages?$filter=isRead eq false and receivedDateTime gt 2025-01-01T00:00:00Z**](https://developer.microsoft.com/graph/graph-explorer?request=me%2Fmessages%3F%24filter%3DisRead%2Beq%2Bfalse%2Band%2BreceivedDateTime%2Bgt%2B2025-01-01T00%3A00%3A00Z\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

**Por remitente:**

[**GET /me/messages?$filter=from/emailAddress/address eq 'test@cursograph.onmicrosoft.com'**](https://developer.microsoft.com/graph/graph-explorer?request=me%2Fmessages%3F%24filter%3Dfrom%2FemailAddress%2Faddress%2Beq%2B%27test%40cursograph.onmicrosoft.com%27\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

**Con attachments:**

[**GET /me/messages?$filter=hasAttachments eq true**](https://developer.microsoft.com/graph/graph-explorer?request=me%2Fmessages%3F%24filter%3DhasAttachments%2Beq%2Btrue\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

**Búsqueda de texto (requiere `$search` y `ConsistencyLevel: eventual`):**

[**GET /me/messages?$search="report.pdf"&$count=true**](https://developer.microsoft.com/graph/graph-explorer?request=me%2Fmessages%3F%24search%3D%22report.pdf%22%26%24count%3Dtrue\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com\&headers=W3sibmFtZSI6IkNvbnNpc3RlbmN5TGV2ZWwiLCJ2YWx1ZSI6ImV2ZW50dWFsIn1d)\
**Header: ConsistencyLevel: eventual**

#### 4. Listar adjuntos de un mensaje

[**GET /me/messages/{messageId}/attachments**](https://developer.microsoft.com/graph/graph-explorer?request=me%2Fmessages%2F%7BmessageId%7D%2Fattachments\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com\&headers=W3sibmFtZSI6IkNvbnNpc3RlbmN5TGV2ZWwiLCJ2YWx1ZSI6ImV2ZW50dWFsIn1d)

\
[**GET /me/messages/{messageId}/attachments/{attachmentId}**](https://developer.microsoft.com/graph/graph-explorer?request=me%2Fmessages%2F%7BmessageId%7D%2Fattachments%2F%7BattachmentId%7D\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com\&headers=W3sibmFtZSI6IkNvbnNpc3RlbmN5TGV2ZWwiLCJ2YWx1ZSI6ImV2ZW50dWFsIn1d)

Para descargar el **contenido** de un archivo:​

[**GET /me/messages/{messageId}/attachments/{attachmentId}/$value**](https://developer.microsoft.com/graph/graph-explorer?request=me%2Fmessages%2F%7BmessageId%7D%2Fattachments%2F%7BattachmentId%7D%2F%24value\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com\&headers=W3sibmFtZSI6IkNvbnNpc3RlbmN5TGV2ZWwiLCJ2YWx1ZSI6ImV2ZW50dWFsIn1d)

Devuelve los **bytes** del archivo (raw content).

#### [Referencia](https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview?view=graph-rest-1.0)

#### 💻 Ejemplos <a href="#ejemplos-en-python-leer-bandeja-filtrar-no-ledo-d" id="ejemplos-en-python-leer-bandeja-filtrar-no-ledo-d"></a>

#### 1. Leer bandeja de entrada con filtros básicos

{% code title="A0\_1\_get\_token.py" overflow="wrap" expandable="true" %}

```python
from dotenv import load_dotenv
from msal import PublicClientApplication
import os

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

def get_delegated_token(scopes, refresh_if_needed: bool = True):
    """Obtener token delegado (usuario presente)."""
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )
    
    # Usar device code flow para interactividad
    result = app.acquire_token_interactive(scopes=scopes)

    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    
    return result["access_token"]
```

{% endcode %}

{% code title="A1\_1\_read\_inbox.py" overflow="wrap" expandable="true" %}

```python
import logging
from datetime import datetime, timedelta, timezone
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Permisos delegados: Mail.Read para leer, Mail.ReadWrite para marcar leído
SCOPES = ["Mail.Read"]

def format_graph_datetime(dt: datetime) -> str:
    """Formato estricto para filtros Graph: YYYY-MM-DDTHH:MM:SSZ sin micros/offset."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def read_inbox_unread(token):
    """Leer mensajes no leídos de la bandeja de entrada."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Filtrar: no leídos, ordenar por fecha descendente
    params = {
        "$filter": "isRead eq false",
        "$orderby": "receivedDateTime desc",
        "$select": "id,subject,from,receivedDateTime,isRead,hasAttachments,bodyPreview",
        "$top": 10,
    }
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    messages = resp.json().get("value", [])
    logger.info(f"Encontrados {len(messages)} mensajes no leídos")
    
    for msg in messages:
        print(f"\n{'='*60}")
        print(f"De: {msg['from']['emailAddress']['name']} <{msg['from']['emailAddress']['address']}>")
        print(f"Asunto: {msg['subject']}")
        print(f"Recibido: {msg['receivedDateTime']}")
        print(f"Adjuntos: {'Sí' if msg['hasAttachments'] else 'No'}")
        print(f"Preview: {msg.get('bodyPreview', 'N/A')[:100]}")
    
    return messages

def read_recent_messages(token, days: int = 1, unread_only: bool = False):
    """Leer mensajes recientes (últimos N días)."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Fecha hace N días
    start_date = format_graph_datetime(datetime.now(timezone.utc) - timedelta(days=days))
    
    # Construir filtro
    filter_expr = f"receivedDateTime gt {start_date}"
    if unread_only:
        filter_expr += " and isRead eq false"
    
    params = {
        "$filter": filter_expr,
        "$orderby": "receivedDateTime desc",
        "$select": "id,subject,from,receivedDateTime,isRead,hasAttachments",
        "$top": 20,
    }
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/messages",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    messages = resp.json().get("value", [])
    logger.info(f"Encontrados {len(messages)} mensajes en los últimos {days} días")
    
    return messages

if __name__ == "__main__":
    logger.info("=== Autenticando ===")
    token = get_delegated_token(SCOPES)

    logger.info("=== Leyendo bandeja de entrada ===")
    messages = read_inbox_unread(token)
    
    logger.info("\n=== Leyendo últimos 3 días (sin leer) ===")
    recent = read_recent_messages(token, days=3, unread_only=True)
```

{% endcode %}

Patrón: filtros combinados, select para reducir datos, paginación.

#### 2. Descargar adjuntos

{% code title="A1\_2\_download\_attachments.py" overflow="wrap" expandable="true" %}

```python
import logging
from pathlib import Path
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["Mail.Read"]

def find_messages_with_attachments(token, limit: int = 5):
    """Encontrar mensajes con adjuntos."""
    headers = {"Authorization": f"Bearer {token}"}
    
    params = {
        "$filter": "hasAttachments eq true",
        "$select": "id,subject,from,hasAttachments",
        "$top": limit,
    }
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/messages",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    return resp.json().get("value", [])

def list_attachments(token: str, message_id: str):
    """Listar adjuntos de un mensaje."""
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments",
        headers=headers,
        timeout=15,
    )
    resp.raise_for_status()
    
    return resp.json().get("value", [])

def download_attachment(token: str, message_id: str, attachment_id: str, filename: str = None):
    """Descargar un adjunto a disco."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener metadata del adjunto
    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments/{attachment_id}",
        headers=headers,
        timeout=15,
    )
    resp.raise_for_status()
    attachment_info = resp.json()
    
    if not filename:
        filename = attachment_info['name']
    
    # Descargar contenido ($value devuelve bytes)
    resp_content = requests.get(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments/{attachment_id}/$value",
        headers=headers,
        timeout=30,  # Archivos grandes pueden tardar
    )
    resp_content.raise_for_status()
    
    # Guardar a disco
    output_path = Path("downloads") / filename
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "wb") as f:
        f.write(resp_content.content)
    
    logger.info(f"✅ Descargado: {output_path} ({len(resp_content.content)} bytes)")
    
    return str(output_path)

def download_all_attachments_from_message(token: str, message_id: str, subject: str):
    """Descargar todos los adjuntos de un mensaje."""
    attachments = list_attachments(token, message_id)
    
    logger.info(f"Descargando {len(attachments)} adjuntos de: '{subject}'")
    
    downloaded = []
    for att in attachments:
        att_id = att['id']
        att_name = att['name']
        att_size = att.get('size', 0)
        
        logger.info(f"  Adjunto: {att_name} ({att_size} bytes)")
        
        path = download_attachment(token, message_id, att_id, att_name)
        downloaded.append(path)
    
    return downloaded

if __name__ == "__main__":
    token = get_delegated_token(SCOPES)
    
    # Paso 1: Encontrar mensajes con adjuntos
    logger.info("=== Buscando mensajes con adjuntos ===")
    messages = find_messages_with_attachments(token, limit=3)
    
    for msg in messages:
        logger.info(f"\nMensaje: {msg['subject']}")
        logger.info(f"De: {msg['from']['emailAddress']['name']}")
        
        # Paso 2: Descargar todos los adjuntos
        downloaded = download_all_attachments_from_message(token, msg['id'], msg['subject'])
        logger.info(f"Descargados {len(downloaded)} archivos")
```

{% endcode %}

Patrón: encontrar, listar, descargar (/$value para bytes).

#### 3. Marcar como leído y procesamiento avanzado

{% code title="A1\_3\_process\_and\_mark\_read.py" overflow="wrap" expandable="true" %}

```python
import os
import logging
import requests
from A1_2_download_attachments import download_all_attachments_from_message
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mail.ReadWrite permite leer Y marcar como leído
SCOPES = ["Mail.ReadWrite"]

def mark_as_read(token: str, message_id: str):
    """Marcar un mensaje como leído."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    body = {"isRead": True}
    
    resp = requests.patch(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}",
        headers=headers,
        json=body,
        timeout=15,
    )
    
    if resp.ok:
        logger.info(f"✅ Mensaje {message_id[:20]}... marcado como leído")
        return True
    else:
        logger.error(f"❌ Error marcando leído: {resp.text}")
        return False

def process_inbox_workflow(token):
    """
    Workflow:
    1. Leer mensajes no leídos
    2. Para cada uno: descargar adjuntos si tiene
    3. Marcar como leído
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    # Paso 1: Listar no leídos
    params = {
        "$filter": "isRead eq false and hasAttachments eq true",
        "$select": "id,subject,from",
        "$top": 5,
    }
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/messages",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    messages = resp.json().get("value", [])
    logger.info(f"Procesando {len(messages)} mensajes no leídos con adjuntos")
    
    for msg in messages:
        msg_id = msg['id']
        subject = msg['subject']
        
        logger.info(f"\n▶ Procesando: {subject}")
        
        download_all_attachments_from_message(token, msg_id, subject)
        
        mark_as_read(token, msg_id)

if __name__ == "__main__":
    token = get_delegated_token(SCOPES)
    process_inbox_workflow(token)
```

{% endcode %}

Patrón: lectura, procesamiento (adjuntos), marcado leído.

#### ✅ Buenas prácticas  <a href="#buenas-prcticas-5-min" id="buenas-prcticas-5-min"></a>

1. **Usar `$select` para reducir datos transferidos**:
   * No traer cuerpo completo si solo necesitas asunto/remitente.
   * El body puede ser muy grande (HTML con imágenes embebidas).​
2. **Combinar filtros con `and`**:
   * `isRead eq false and hasAttachments eq true and receivedDateTime gt ...`
   * Más eficiente que leer todo y filtrar en cliente.​
3. **Verificar `hasAttachments` antes de llamar a `/attachments`**:
   * Ahorra peticiones si no hay adjuntos.
4. **Tamaños de adjuntos y límites**:
   * Adjuntos típicamente tienen límite de **150 MB**.
   * Considerar cortes de conexión con archivos muy grandes.
   * Usar reintentos con backoff para descargas largas.
5. **Encoding de caracteres**:
   * Algunos asuntos/cuerpos pueden estar en MIME encoded (`=?UTF-8?B?...?=`).
   * Python `email.header` puede decodificar si necesario
6. **Respeto a privacidad**:
   * No loguear contenidos completos de mensajes (PII).
   * Ser cuidadoso con descarga de adjuntos en automatización.
7. **Paginación con `@odata.nextLink`**:
   * Bandeja de entrada puede tener miles de mensajes.
   * Seguir links de paginación, no confiar en `$top`
8. **Diferencia entre `/me` y `/users/{userId}`**:
   * `/me` usa contexto del usuario autenticado (delegated).
   * `/users/{userId}` requiere permisos más altos (app-only, o delegated como admin)​

#### 🎓 <mark style="color:$primary;">Ejercicios</mark>  <a href="#ejercicios-guiados-3-min" id="ejercicios-guiados-3-min"></a>

#### <mark style="color:$primary;">Ejercicio 1: Leer y resumir no leídos</mark>

<mark style="color:$primary;">Crear script que, en bucle infinito:</mark>

1. <mark style="color:$primary;">Lee últimos 10 mensajes no leídos.</mark>
2. <mark style="color:$primary;">Muestra: De, Asunto, Fecha, Tiene adjuntos (Sí/No).</mark>
3. <mark style="color:$primary;">Resume en una tabla.</mark>
4. <mark style="color:$primary;">Espera 10 segundos</mark>

<mark style="color:$primary;">Probar enviando un correo una vez lanzado el script</mark>

#### <mark style="color:$primary;">Ejercicio 2: Descargar attachments de la semana</mark>

<mark style="color:$primary;">Caso: descargar todos los adjuntos de correos recibidos en la última semana.</mark>

1. <mark style="color:$primary;">Calcular fecha de hace una semana.</mark>
2. <mark style="color:$primary;">Filtrar mensajes</mark>&#x20;
3. <mark style="color:$primary;">Descargar todos los adjuntos a carpeta local.</mark>
4. <mark style="color:$primary;">Loguear qué se descargó.</mark>

#### <mark style="color:$primary;">Ejercicio 3: Workflow de triage</mark>

<mark style="color:$primary;">Simular un "triage" simple:</mark>

1. <mark style="color:$primary;">Leer mensajes de remitentes específicos (buscar por email en</mark> <mark style="color:$primary;"></mark><mark style="color:$primary;">`from/emailAddress/address`</mark><mark style="color:$primary;">).</mark>
2. <mark style="color:$primary;">Los no leídos: descargar adjuntos si tienen.</mark>
3. <mark style="color:$primary;">Marcar como leído.</mark>
4. <mark style="color:$primary;">Reportar: "5 procesados, 2 con adjuntos descargados".</mark>

***

### Envío de correos (texto/HTML) y buenas prácticas de formato

#### Draft vs Send

En Outlook/Exchange, hay dos formas de trabajar con correos

**Opción 1: Crear como borrador, luego enviar**

1. **`POST /messages`** → crea un mensaje en Drafts.
2. **`POST /messages/{id}/send`** → envía el borrador.

Ventajas:

* Permite ediciones parciales, validaciones.
* Más control: puedes guardar borradores intermedios.

**Opción 2: Enviar directamente**

**`POST /sendMail`** → crea y envía en una sola operación.

Ventajas:

* Más simple, menos overhead.
* Directo si no necesitas editar antes.

#### Tipos de contenido: texto vs HTML

La propiedad `body` tiene estructura:

```json
{
  "contentType": "text|html",
  "content": "..."
}
```

**Text:**

* Contenido plano, sin formato.
* Seguro: no hay riesgo de scripts o imágenes embebidas.
* Recomendado para correos automatizados simples.

**HTML:**

* Permite formato, colores, imágenes embebidas.
* Mayor flexibilidad visual.
* **Riesgo:** XSS (cross-site scripting) si no se sanitiza.

#### Consideraciones de seguridad

**Prevención de phishing:**

* No suplantar remitentes (el "From" es fijo al usuario autenticado).
* Validar direcciones de correo destino (evitar typosquatting).
* No incluir enlaces sospechosos sin verificación.

**HTML seguro:**

* Sanitizar contenido HTML (remover scripts, handlers JavaScript).
* Usar librerías como `bleach` en Python para limpiar HTML.

**Rate limiting:**

* No enviar spam masivo (riesgo de throttling 429).
* Respetar límites de Graph: típicamente 10-30 emails por minuto por usuario

#### 1. Crear draft

{% code overflow="wrap" expandable="true" %}

```json
POST /me/messages
Content-Type: application/json

{
  "subject": "Reunión Mañana",
  "body": {
    "contentType": "text",
    "content": "Hablemos de los resultados de 1T."
  },
  "toRecipients": [
    {
      "emailAddress": {
        "address": "juan@cursograph.onmicrosoft.com",
        "name": "Juan Pérez"
      }
    }
  ],
  "ccRecipients": [...],
  "bccRecipients": [...],
  "categories": ["work", "follow-up"],
  "importance": "high"
}
```

{% endcode %}

Devuelve message object con `id`. Se guarda en Drafts.

#### 2. Enviar draft

```shellscript
POST /me/messages/{messageId}/send
```

Sin body. Envía el mensaje guardado y lo mueve a SentItems.

#### 3. Enviar directamente (sendMail)

{% code overflow="wrap" expandable="true" %}

```shellscript
POST /me/sendMail
Content-Type: application/json

{
  "message": {
    "subject": "Quick Update",
    "body": {
      "contentType": "html",
      "content": "<p>Check this <b>important</b> info.</p>"
    },
    "toRecipients": [
      {
        "emailAddress": {
          "address": "test@cursograph.onmicrosoft.com"
        }
      }
    ]
  },
  "saveToSentItems": true
}
```

{% endcode %}

Envía directamente. **`saveToSentItems`** (opcional, default true) guarda copia en enviados.​

#### 4. Agregar attachments

Para mensajes con adjuntos, primero crear como draft, luego agregar attachments vía endpoint separado:​

{% code overflow="wrap" expandable="true" %}

```shellscript
POST /me/messages/{messageId}/attachments
Content-Type: application/json

{
  "@odata.type": "#microsoft.graph.fileAttachment",
  "name": "report.pdf",
  "contentBytes": "<base64-encoded-content>"
}
```

{% endcode %}

O para item attachments (Outlook items):

{% code overflow="wrap" expandable="true" %}

```shellscript
{
  "@odata.type": "#microsoft.graph.itemAttachment",
  "name": "Meeting Notes",
  "item": { ... }
}
```

{% endcode %}

#### 5. Recipients y validación

Estructura de recipient:

{% code overflow="wrap" expandable="true" %}

```shellscript
{
  "emailAddress": {
    "address": "user@contoso.com",
    "name": "User Name"  // opcional
  }
}
```

{% endcode %}

* **toRecipients**: destinatarios principales.
* **ccRecipients**: con copia.
* **bccRecipients**: con copia oculta.
* **replyTo**: dirección de respuesta (opcional).

#### 6. Categorías e importancia

**Categorías:** Array de strings: `["work", "personal", "follow-up"]`.

**Importancia: "**&#x6E;ormal", "high", "low".

#### 💻 Ejemplos  <a href="#ejemplos-en-python-envo-simple-html-con-attachmen" id="ejemplos-en-python-envo-simple-html-con-attachmen"></a>

#### 1. Envío simple (texto)

{% code title="A2\_1\_send\_simple\_email.py" overflow="wrap" expandable="true" %}

```python
import logging
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mail.Send permite enviar correos
SCOPES = ["Mail.Send"]

def send_simple_email(to_address: str, subject: str, body_text: str):
    """Enviar correo simple (texto)."""
    token = get_delegated_token(SCOPES)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "text",
                "content": body_text,
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": to_address,
                    }
                }
            ],
        },
        "saveToSentItems": True,
    }
    
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/me/sendMail",
        headers=headers,
        json=payload,
        timeout=15,
    )
    
    if resp.status_code == 202:  # 202 Accepted (envío en background)
        logger.info(f"✅ Correo enviado a {to_address}")
        return True
    else:
        logger.error(f"❌ Error enviando correo: {resp.text}")
        return False

if __name__ == "__main__":
    send_simple_email(
        to_address="test@cursograph.onmicrosoft.com",
        subject="Reunión Mañana",
        body_text="Hablemos del curso.\n\nChao",
    )
```

{% endcode %}

Status 202 indica envío aceptado (asincrono).

#### 2. Envío HTML con validación

{% code title="A2\_2\_send\_html\_email.py" overflow="wrap" expandable="true" %}

```python
import logging
import re
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["Mail.Send"]

def validate_email(email: str) -> bool:
    """Validar formato de email básico."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def sanitize_html(html_content: str) -> str:
    """Sanitizar HTML básico (remover scripts peligrosos)."""
    # Esta es una sanitización muy simple; para producción usar bleach library
    import re
    
    # Remover <script> tags
    html_content = re.sub(r"<script.*?</script>", "", html_content, flags=re.DOTALL)
    # Remover event handlers (onclick, onerror, etc.)
    html_content = re.sub(r'\s+on\w+\s*=\s*["\'].*?["\']', "", html_content)
    
    return html_content

def send_html_email(
    to_addresses: list,
    cc_addresses: list,
    subject: str,
    html_body: str,
    importance: str = "normal",
):
    """Enviar correo HTML con validación."""
    
    # Validar direcciones
    for email in to_addresses + cc_addresses:
        if not validate_email(email):
            logger.error(f"❌ Email inválido: {email}")
            return False
    
    # Sanitizar HTML
    html_body = sanitize_html(html_body)
    
    token = get_delegated_token(SCOPES)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    # Construir recipients
    to_recipients = [
        {"emailAddress": {"address": addr}} for addr in to_addresses
    ]
    cc_recipients = [
        {"emailAddress": {"address": addr}} for addr in cc_addresses
    ] if cc_addresses else []
    
    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "html",
                "content": html_body,
            },
            "toRecipients": to_recipients,
            "ccRecipients": cc_recipients,
            "importance": importance,  # normal, high, low
            "categories": ["sent-via-api"],
        },
        "saveToSentItems": True,
    }
    
    logger.info(f"Enviando correo HTML a {len(to_addresses)} destinatarios...")
    
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/me/sendMail",
        headers=headers,
        json=payload,
        timeout=15,
    )
    
    if resp.status_code == 202:
        logger.info(f"✅ Correo HTML enviado")
        return True
    else:
        logger.error(f"❌ Error: {resp.text}")
        return False

if __name__ == "__main__":
    html_content = """
    <html>
    <body>
        <h2>Reporte Trimestral</h2>
        <p>Estimado usuario,</p>
        <p>Adjunto encontrarás el <b>reporte de Q1</b> con los siguientes puntos:</p>
        <ul>
            <li>Ventas: +15%</li>
            <li>Nuevos clientes: 42</li>
            <li>Retención: 98%</li>
        </ul>
        <p>Cualquier pregunta, contáctame.</p>
        <p>Saludos,<br/>El equipo</p>
    </body>
    </html>
    """
    
    send_html_email(
        to_addresses=["test@cursograph.onmicrosoft.com", "diego.montoliu@cursograph.onmicrosoft.com"],
        cc_addresses=["jefe@cursograph.onmicrosoft.com"],
        subject="Reporte Q1 - Datos Clave",
        html_body=html_content,
        importance="high",
    )
```

{% endcode %}

Patrón: validación, sanitización, HTML seguro, múltiples destinatarios.

#### 3. Envío con draft + attachments

{% code title="A2\_3\_send\_with\_attachments.py" overflow="wrap" expandable="true" %}

```python
import base64
import logging
import requests
from pathlib import Path
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["Mail.Send"]

def create_draft(token: str, to_address: str, subject: str, body_text: str):
    """Crear borrador."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "subject": subject,
        "body": {
            "contentType": "text",
            "content": body_text,
        },
        "toRecipients": [
            {"emailAddress": {"address": to_address}}
        ],
    }
    
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/me/messages",
        headers=headers,
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()
    
    message = resp.json()
    logger.info(f"✅ Borrador creado: {message['id']}")
    
    return message['id']

def add_attachment(token: str, message_id: str, file_path: str):
    """Agregar adjunto a un mensaje."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    # Leer archivo y encodear en base64
    with open(file_path, "rb") as f:
        file_content = f.read()
    
    content_bytes = base64.b64encode(file_content).decode()
    filename = Path(file_path).name
    
    payload = {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": filename,
        "contentBytes": content_bytes,
    }
    
    resp = requests.post(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments",
        headers=headers,
        json=payload,
        timeout=30,  # Archivos grandes pueden tardar
    )
    resp.raise_for_status()
    
    logger.info(f"✅ Adjunto '{filename}' agregado")

def send_message(token: str, message_id: str):
    """Enviar un borrador."""
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.post(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/send",
        headers=headers,
        timeout=15,
    )
    
    if resp.status_code == 202:
        logger.info(f"✅ Correo enviado")
        return True
    else:
        logger.error(f"❌ Error: {resp.text}")
        return False

def send_email_with_attachments(to_address: str, subject: str, body_text: str, file_paths: list):
    """Workflow completo: crear draft, agregar adjuntos, enviar."""
    token = get_delegated_token(SCOPES)
    
    try:
        # Paso 1: Crear draft
        msg_id = create_draft(token, to_address, subject, body_text)
        
        # Paso 2: Agregar adjuntos
        for file_path in file_paths:
            if Path(file_path).exists():
                add_attachment(token, msg_id, file_path)
            else:
                logger.warning(f"⚠️ Archivo no encontrado: {file_path}")
        
        # Paso 3: Enviar
        send_message(token, msg_id)
        
        logger.info("✅ Flujo completo exitoso")
        return True
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    send_email_with_attachments(
        to_address="test@cursograph.onmicrosoft.com",
        subject="Documentos Importantes",
        body_text="Adjunto encontrarás los documentos solicitados.",
        file_paths=[
            "report.pdf",
            "data.xlsx",
        ],
    )
```

{% endcode %}

Patrón: draft → attachments → send (workflow de 3 pasos).

#### ✅ Buenas prácticas <a href="#buenas-prcticas-5-min" id="buenas-prcticas-5-min"></a>

1. **Usar Mail.Send (no Mail.ReadWrite) para envío**:
   * Principio de menor privilegio.
   * Mail.Send solo permite enviar, no leer.​
2. **Sanitizar HTML antes de enviar**:
   * Usar librerías como `bleach` para remover scripts y handlers JavaScript.
   * Prevenir XSS y phishing.
3. **Validar direcciones de correo destino**:
   * Comprobar formato válido.
   * Evitar typosquatting ([john@delta-ai.com](mailto:john@contoso.com) vs [john@delta-ai.co](mailto:john@contoso.co)).
4. **No enviar spam masivo**:
   * Respetar límites de Rate: típicamente 10-30 emails/min por usuario.
   * Si necesitas más, considerar usar servicios de Mail (SendGrid, etc.).
5. **Usar texto en lugar de HTML cuando sea posible**:
   * Más seguro.
   * Más rápido.
   * Solo usar HTML si realmente necesitas formato.​
6. **Codificar attachments correctamente (base64)**:
   * Archivos binarios deben estar en base64.
   * Validar tamaño (típicamente < 150 MB).
7. **Status 202 vs 200**:
   * `/sendMail` devuelve 202 (Accepted, asincrono).
   * No esperes sincronía; el correo se envía en background.
8. **Categorías y follow-up**:
   * Usar categorías para organizar correos enviados vía API ("sent-via-api", etc.).
   * Facilita auditoría y seguimiento.​
9. **Pruebas en draft antes de enviar en producción**:
   * Crear algunos drafts, validar formato, luego enviar.
   * Evita errores masivos en producción.​
10. **Logging de envíos**:
    * Registrar: destinatario, asunto, hora, estado.
    * Útil para auditoría, troubleshooting, compliance.

#### <mark style="color:$primary;">🎓 Ejercicios</mark> <a href="#ejercicios-guiados-3-min" id="ejercicios-guiados-3-min"></a>

#### <mark style="color:$primary;">Ejercicio 1: Envío con validación</mark>

<mark style="color:$primary;">Crear script que:</mark>

1. <mark style="color:$primary;">Pida por input: dirección destino, asunto, cuerpo, adjunto.</mark>
2. <mark style="color:$primary;">Valide que la dirección sea de un miembro del curso (formato email, o script con llamada a /users).</mark>
3. <mark style="color:$primary;">Valide que el adjunto existe</mark>
4. <mark style="color:$primary;">Envíe con importancia Alta</mark>
5. <mark style="color:$primary;">Loguee resultado.</mark>

#### <mark style="color:$primary;">Ejercicio 2: Correo HTML formateado</mark>

<mark style="color:$primary;">Crear template HTML para "Notificación de Evento" que incluya:</mark>

* <mark style="color:$primary;">Título (h2).</mark>
* <mark style="color:$primary;">Descripción (párrafos).</mark>
* <mark style="color:$primary;">Detalles en tabla (fecha, hora, ubicación).</mark>
* <mark style="color:$primary;">Link a página de la empresa (href).</mark>
* <mark style="color:$primary;">Firma.</mark>

<mark style="color:$primary;">Probar</mark>

***

### Eventos de calendario: crear, actualizar, cancelar y consultar

#### Estructura de calendarios

En Outlook, cada usuario tiene múltiples calendarios:

* **Calendario principal** (Calendar): el por defecto.
* **Calendarios compartidos**: calendarios delegados de otros usuarios.
* **Calendarios de grupo**: calendarios de equipos/grupos.
* **Calendarios subscritos**: p.ej. feriados públicos.

Acceso vía Graph:

[**GET /me/calendars**](https://developer.microsoft.com/graph/graph-explorer?request=me%2Fcalendars\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

\
[**GET /me/calendarGroups**](https://developer.microsoft.com/graph/graph-explorer?request=me%2FcalendarGroups\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)<br>

#### Propiedades clave de un evento

{% code overflow="wrap" expandable="true" %}

```json
{
  "id": "AAMkADA1M-z...",
  "subject": "Team Meeting",
  "bodyPreview": "Quarterly review discussion",
  "start": {
    "dateTime": "2025-02-15T10:00:00",
    "timeZone": "Europe/Madrid"
  },
  "end": {
    "dateTime": "2025-02-15T11:00:00",
    "timeZone": "Europe/Madrid"
  },
  "location": {
    "displayName": "Conference Room B"
  },
  "attendees": [
    {
      "emailAddress": {
        "address": "john@contoso.com",
        "name": "John Doe"
      },
      "type": "required|optional|resource",
      "status": {
        "response": "accepted|declined|tentativelyAccepted|notResponded",
        "time": "2025-02-14T15:30:00Z"
      }
    }
  ],
  "organizer": {
    "emailAddress": {
      "address": "alice@contoso.com",
      "name": "Alice Smith"
    }
  },
  "recurrence": {
    "pattern": {
      "type": "daily|weekly|absoluteMonthly|relativeMonthly|absoluteYearly|relativeYearly",
      "interval": 1,
      "daysOfWeek": ["monday", "wednesday", "friday"],
      "firstDayOfWeek": "sunday"
    },
    "range": {
      "type": "endDate|noEnd|numbered",
      "startDate": "2025-02-15",
      "endDate": "2025-12-31",
      "recurrenceTimeZone": "Europe/Madrid",
      "numberOfOccurrences": 10
    }
  },
  "isReminderOn": true,
  "reminderMinutesBeforeStart": 15,
  "isOnlineMeeting": true,
  "onlineMeeting": {
    "conferenceProvider": "teamsForBusiness",
    "joinUrl": "https://teams.microsoft.com/..."
  },
  "status": "confirmed|cancelled|tentativelyConfirmed"
}
```

{% endcode %}

#### Time zones

Graph soporta time zones estándar IANA (p.ej. "America/New\_York", "Europe/London"):

* Importante para eventos de múltiples zonas.
* El servidor calcula conversiones automáticamente.
* Siempre usar time zone explícitamente (no asumir UTC).

#### Recurrencia

Patrón + rango definen recurrencia:

* **Pattern types**: daily, weekly, monthly, yearly.
* **Range types**: endDate (hasta fecha), noEnd (infinito), numbered (N ocurrencias).
* Ejemplo: "cada lunes, miércoles y viernes hasta fin de año".

#### 1. Crear evento

<pre class="language-shellscript" data-overflow="wrap" data-expandable="true"><code class="lang-shellscript"><strong>POST /me/events
</strong>Content-Type: application/json

{
  "subject": "Team Meeting",
  "start": {
    "dateTime": "2025-02-15T10:00:00",
    "timeZone": "Europe/Madrid"
  },
  "end": {
    "dateTime": "2025-02-15T11:00:00",
    "timeZone": "Europe/Madrid"
  },
  "location": {
    "displayName": "Conference Room B"
  },
  "attendees": [
    {
      "emailAddress": {
        "address": "test@cursograph.onmicrosoft.com",
        "name": "Test Curso"
      },
      "type": "required"
    }
  ],
  "isReminderOn": true,
  "reminderMinutesBeforeStart": 15
}
</code></pre>

Devuelve el evento creado con `id`.

Con recurrencia:

<pre class="language-json" data-overflow="wrap" data-expandable="true"><code class="lang-json">{
  "subject": "Weekly Standup",
  "start": { ... },
  "end": { ... },
<strong>  "recurrence": {
</strong>    "pattern": {
      "type": "weekly",
      "interval": 1,
      "daysOfWeek": ["monday", "tuesday", "wednesday", "thursday", "friday"]
    },
    "range": {
      "type": "endDate",
      "startDate": "2025-02-17",
      "endDate": "2025-12-31"
    }
  }
}
</code></pre>

#### 2. Actualizar evento

<pre class="language-shellscript" data-overflow="wrap" data-expandable="true"><code class="lang-shellscript"><strong>PATCH /me/events/{eventId}
</strong>Content-Type: application/json

{
  "subject": "Team Meeting (Rescheduled)",
  "start": {
    "dateTime": "2025-02-15T14:00:00",
    "timeZone": "Europe/Madrid"
  }
}
</code></pre>

Solo cambias los campos que se necesiten actualizar.

#### 3. Cancelar evento

<pre class="language-shellscript" data-overflow="wrap" data-expandable="true"><code class="lang-shellscript"><strong>POST /me/events/{eventId}/cancel
</strong>Content-Type: application/json

{
  "comment": "Reunión pospuesta para próxima semana"
}
</code></pre>

El evento se marca como `cancelled` y se notifica a asistentes.

#### 4. Listar eventos (calendarView)

[**GET /me/calendarview?startDateTime=2025-02-01T00:00:00Z\&endDateTime=2025-02-28T23:59:59Z**](https://developer.microsoft.com/graph/graph-explorer?request=me%2Fcalendarview%3FstartDateTime%3D2025-02-01T00%3A00%3A00Z%26endDateTime%3D2025-02-28T23%3A59%3A59Z\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

Devuelve eventos en rango de fechas (incluso ocurrencias de recurrencia expandidas).

Con filtros:

[**GET /me/events?$filter=start/dateTime ge '2025-02-15' and end/dateTime le '2025-02-20'**\
**&$select=subject,start,end,organizer,attendees**\
**&$orderby=start/dateTime**\
**&$top=20**](https://developer.microsoft.com/graph/graph-explorer?request=me%2Fcalendarview%3FstartDateTime%3D2025-02-01T00%3A00%3A00Z%26endDateTime%3D2025-02-28T23%3A59%3A59Z\&method=GET\&version=v1.0\&GraphUrl=https://graph.microsoft.com)

#### [**Referencia**](https://learn.microsoft.com/en-us/graph/outlook-calendar-concept-overview?view=graph-rest-1.0)

#### 💻 Ejemplos <a href="#ejemplos-en-python-crud-completo-recurrencia-time" id="ejemplos-en-python-crud-completo-recurrencia-time"></a>

#### 1. Crear evento simple

{% code title="A3\_1\_create\_event.py" overflow="wrap" expandable="true" %}

```python
import logging
from datetime import datetime, timedelta
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Calendars.ReadWrite permite crear/modificar eventos
SCOPES = ["Calendars.ReadWrite"]

def create_event(
    subject: str,
    start_time: str,  # ISO format: "2025-02-15T10:00:00"
    end_time: str,
    time_zone: str = "Europe/Madrid",
    location: str = None,
    attendees: list = None,
    is_online_meeting: bool = False,
):
    """Crear evento simple."""
    token = get_delegated_token(SCOPES)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "subject": subject,
        "start": {
            "dateTime": start_time,
            "timeZone": time_zone,
        },
        "end": {
            "dateTime": end_time,
            "timeZone": time_zone,
        },
        "isReminderOn": True,
        "reminderMinutesBeforeStart": 15,
    }
    
    if location:
        payload["location"] = {"displayName": location}
    
    if attendees:
        payload["attendees"] = [
            {
                "emailAddress": {
                    "address": addr,
                    "name": addr.split("@")[0],  # Usar parte antes de @
                },
                "type": "required",
            }
            for addr in attendees
        ]
    
    if is_online_meeting:
        payload["isOnlineMeeting"] = True
        payload["onlineMeetingProvider"] = "teamsForBusiness"
    
    logger.info(f"Creando evento: {subject}")
    
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/me/events",
        headers=headers,
        json=payload,
        timeout=15,
    )
    
    if resp.ok:
        event = resp.json()
        logger.info(f"✅ Evento creado: {event['id']}")
        logger.info(f"   URL Teams: {event.get('onlineMeeting', {}).get('joinUrl', 'N/A')}")
        return event
    else:
        logger.error(f"❌ Error: {resp.text}")
        return None

if __name__ == "__main__":
    create_event(
        subject="Team Meeting",
        start_time="2025-02-15T10:00:00",
        end_time="2025-02-15T11:00:00",
        time_zone="America/New_York",
        location="Conference Room B",
        attendees=["john@contoso.com", "jane@contoso.com"],
        is_online_meeting=True,
    )
```

{% endcode %}

Patrón: estructura clara, time zone explícito, Teams meeting.

#### 2. Crear evento recurrente

{% code title="A3\_1\_create\_recurring\_event.py" overflow="wrap" expandable="true" %}

```python
import logging
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["Calendars.ReadWrite"]

def create_recurring_event(
    subject: str,
    start_date: str,  # "2025-02-17"
    start_time: str,  # "09:00:00"
    end_time: str,    # "10:00:00"
    time_zone: str,
    days_of_week: list,  # ["monday", "tuesday", ...]
    end_date: str,  # "2025-12-31" o None para infinito
):
    """Crear evento recurrente."""
    token = get_delegated_token(SCOPES)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    # Construir datetime
    start_datetime = f"{start_date}T{start_time}"
    end_datetime = f"{start_date}T{end_time}"
    
    payload = {
        "subject": subject,
        "start": {
            "dateTime": start_datetime,
            "timeZone": time_zone,
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": time_zone,
        },
        "recurrence": {
            "pattern": {
                "type": "weekly",
                "interval": 1,
                "daysOfWeek": days_of_week,
                "firstDayOfWeek": "sunday",
            },
            "range": {
                "type": "endDate" if end_date else "noEnd",
                "startDate": start_date,
                "endDate": end_date,
                "recurrenceTimeZone": time_zone,
            },
        },
        "isReminderOn": True,
        "reminderMinutesBeforeStart": 10,
    }
    
    logger.info(f"Creando evento recurrente: {subject}")
    
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/me/events",
        headers=headers,
        json=payload,
        timeout=15,
    )
    
    if resp.ok:
        event = resp.json()
        logger.info(f"✅ Evento recurrente creado: {event['id']}")
        logger.info(f"   Patrón: {', '.join(days_of_week)} de {start_date} hasta {end_date or 'sin fin'}")
        return event
    else:
        logger.error(f"❌ Error: {resp.text}")
        return None

if __name__ == "__main__":
    create_recurring_event(
        subject="Weekly Standup",
        start_date="2025-02-17",
        start_time="09:00:00",
        end_time="09:30:00",
        time_zone="Europe/Madrid",
        days_of_week=["monday", "tuesday", "wednesday", "thursday", "friday"],
        end_date="2025-12-31",
    )
```

{% endcode %}

Patrón: recurrence pattern + range, time zone consistente.

#### 3. CRUD completo: actualizar y cancelar

{% code title="A3\_3\_event\_crud.py" overflow="wrap" expandable="true" %}

```python
import logging
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["Calendars.ReadWrite"]

def update_event(token: str, event_id: str, **changes):
    """Actualizar evento (cambios parciales)."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = changes
    
    logger.info(f"Actualizando evento {event_id}...")
    
    resp = requests.patch(
        f"https://graph.microsoft.com/v1.0/me/events/{event_id}",
        headers=headers,
        json=payload,
        timeout=15,
    )
    
    if resp.ok:
        logger.info(f"✅ Evento actualizado")
        return resp.json()
    else:
        logger.error(f"❌ Error: {resp.text}")
        return None

def cancel_event(token: str, event_id: str, comment: str = None):
    """Cancelar evento."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {}
    if comment:
        payload["comment"] = comment
    
    logger.info(f"Cancelando evento {event_id}...")
    
    resp = requests.post(
        f"https://graph.microsoft.com/v1.0/me/events/{event_id}/cancel",
        headers=headers,
        json=payload,
        timeout=15,
    )
    
    if resp.status_code == 200:
        logger.info(f"✅ Evento cancelado")
        return True
    else:
        logger.error(f"❌ Error: {resp.text}")
        return False

def list_upcoming_events(token: str, days_ahead: int = 7):
    """Listar próximos eventos."""
    headers = {"Authorization": f"Bearer {token}"}
    
    from datetime import datetime, timedelta
    
    start = datetime.utcnow().isoformat() + "Z"
    end = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + "Z"
    
    params = {
        "startDateTime": start,
        "endDateTime": end,
        "$select": "subject,start,end,organizer,attendees",
        "$orderby": "start/dateTime",
        "$top": 20,
    }
    
    logger.info(f"Listando eventos próximos {days_ahead} días...")
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/calendarview",
        headers=headers,
        params=params,
        timeout=15,
    )
    
    if resp.ok:
        events = resp.json().get("value", [])
        logger.info(f"✅ {len(events)} eventos encontrados")
        
        for event in events:
            print(f"\n{event['subject']}")
            print(f"  Inicio: {event['start']['dateTime']}")
            print(f"  Fin: {event['end']['dateTime']}")
            print(f"  Organizador: {event['organizer']['emailAddress']['name']}")
            print(f"  Asistentes: {len(event.get('attendees', []))}")
        
        return events
    else:
        logger.error(f"❌ Error: {resp.text}")
        return []

if __name__ == "__main__":
    token = get_delegated_token(SCOPES)
    
    # Listar próximos eventos
    events = list_upcoming_events(token, days_ahead=14)
    
    if events:
        # Actualizar el primero
        event_id = events[0]['id']
        update_event(token, event_id, subject=f"{events[0]['subject']} (UPDATED)")
        
        # Cancelar (comentado por seguridad)
        # cancel_event(token, event_id, comment="Cambio de planes")
```

{% endcode %}

Patrón: CRUD completo, time zone consistente, manejo de errores.

#### ✅ Buenas prácticas <a href="#buenas-prcticas-5-min" id="buenas-prcticas-5-min"></a>

1. **Siempre especificar time zone explícitamente**:
   * No asumir UTC; usar time zones IANA ("America/New\_York", no "-5:00").
   * Importante para usuarios globales y recurrencias.
2. **Usar `calendarview` en lugar de `events` para rangos de fechas**:
   * `/calendarview` expande recurrencias automáticamente.
   * `/events` devuelve solo eventos maestros (no ocurrencias).
3. **Validar conflictos antes de crear**:
   * Consultar eventos existentes en el rango de tiempo.
   * Avisar si hay conflictos antes de confirmar creación.
4. **Usar `isOnlineMeeting` y `onlineMeetingProvider`**:
   * Automáticamente crea reunión de Teams.
   * Los asistentes reciben link de unión.
5. **Notificaciones coherentes**:
   * `isReminderOn: true` + `reminderMinutesBeforeStart: 15` por defecto.
   * Adaptar según criticidad del evento.
6. **Roles de asistentes**:
   * `required`: obligatorio asistir.
   * `optional`: opcional.
   * `resource`: recurso (sala de conferencias).
7. **Status de eventos y respuestas**:
   * Event `status`: "confirmed", "cancelled", "tentativelyConfirmed".
   * Attendee `response`: "accepted", "declined", "tentativelyAccepted", "notResponded".
8. **Separar organizer de asistentes**:
   * Organizer es creador, tiene permisos plenos.
   * Asistentes solo pueden responder (aceptar/declinar).
9. **Recurrencia: usar pattern + range claramente**:
   * Pattern (qué días/intervalos).
   * Range (cuándo termina).
   * Deben estar coordinados lógicamente.
10. **Loguear todas las operaciones de calendario**:
    * Crear, actualizar, cancelar: auditoría importante.
    * Incluir organizer, asistentes, cambios realizados.

#### <mark style="color:$primary;">🎓 Ejercicios</mark> <a href="#ejercicios-guiados-3-min" id="ejercicios-guiados-3-min"></a>

#### <mark style="color:$primary;">Ejercicio 1: Crear evento simple con equipos</mark>

1. <mark style="color:$primary;">Crear evento "Team Sync" para el próximo lunes a las 10:00 AM.</mark>
2. <mark style="color:$primary;">Duración: 30 minutos.</mark>
3. <mark style="color:$primary;">Invitar a 2 compañeros (addresses).</mark>
4. <mark style="color:$primary;">Verificar que se creó correctamente listando calendarview.</mark>

#### <mark style="color:$primary;">Ejercicio 2: Crear serie semanal</mark>

<mark style="color:$primary;">Caso: "Daily Standup" cada lunes a viernes, 9:00-9:15 AM, durante 3 meses.</mark>

1. <mark style="color:$primary;">Crear evento recurrente.</mark>
2. <mark style="color:$primary;">Pattern: weekly, lunes-viernes.</mark>
3. <mark style="color:$primary;">Range: 3 meses desde hoy.</mark>
4. <mark style="color:$primary;">Time zone correcto (su región).</mark>
5. <mark style="color:$primary;">Verificar listando 5-10 ocurrencias.</mark>

#### <mark style="color:$primary;">Ejercicio 3: Actualizar y cancelar</mark>

<mark style="color:$primary;">Dado un evento existente:</mark>

1. <mark style="color:$primary;">Cambiar subject y hora (actualización PATCH).</mark>
2. <mark style="color:$primary;">Listar nuevamente para confirmar cambio.</mark>
3. <mark style="color:$primary;">Cancelar el evento con comentario.</mark>
4. <mark style="color:$primary;">Verificar que aparece como "cancelled".</mark>

***

### Consultas por rango de fechas y vistas de calendario

#### 1. Endpoints Fundamentales: `/events` vs `/calendarView`&#x20;

#### Diferencia Clave

Microsoft Graph ofrece dos endpoints para acceder a eventos, cada uno con comportamientos distintos:

<table data-header-hidden><thead><tr><th width="198"></th><th></th><th></th></tr></thead><tbody><tr><td>Aspecto</td><td><code>/</code><strong><code>events</code></strong></td><td><code>/</code><strong><code>calendarView</code></strong></td></tr><tr><td><strong>Eventos Recurrentes</strong></td><td>Solo devuelve la serie maestra</td><td>Expande todas las instancias</td></tr><tr><td><strong>Rango de Fechas</strong></td><td>Usa <code>$filter</code></td><td>Usa <code>startDateTime</code> y <code>endDateTime</code></td></tr><tr><td><strong>Mejor para</strong></td><td>Búsquedas simples, eventos individuales</td><td>Vistas de calendario completas</td></tr><tr><td><strong>Rendimiento</strong></td><td>Más rápido para rangos pequeños</td><td>Optimizado para rangos amplios</td></tr></tbody></table>

#### Estructura de Endpoints

{% code overflow="wrap" expandable="true" %}

```shellscript
# Para el calendario predeterminado del usuario
GET /me/calendarView?startDateTime={datetime}&endDateTime={datetime}
GET /me/calendar/events?$filter=...

# Para un usuario específico
GET /users/{userId}/calendarView?startDateTime={datetime}&endDateTime={datetime}
GET /users/{userId}/calendar/events?$filter=...

# Para calendarios específicos
GET /me/calendars/{calendarId}/calendarView?startDateTime={datetime}&endDateTime={datetime}
```

{% endcode %}

#### 2. Consultas por Rango de Fechas

#### Método 1: Usando `/calendarView` (Recomendado)

El endpoint `calendarView` es la forma preferida para obtener eventos dentro de un rango. Expande automáticamente eventos recurrentes.

**Parámetros obligatorios:**

* `startDateTime`: Fecha y hora de inicio (ISO 8601)
* `endDateTime`: Fecha y hora de fin (ISO 8601)

{% code title="A4\_1\_filter\_calendar\_view\.py" overflow="wrap" expandable="true" %}

```python
import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

# Configuración
SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Definir rango de fechas (próximos 7 días)
start_date = datetime.now(timezone.utc)
end_date = start_date + timedelta(days=7)

# Formatear en ISO 8601 UTC
start_datetime = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
end_datetime = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

# URL del endpoint
url = "https://graph.microsoft.com/v1.0/me/calendarView"

# Parámetros de la consulta
params = {
    "startDateTime": start_datetime,
    "endDateTime": end_datetime,
    "$top": 25,  # Paginación
    "$orderby": "start/dateTime"  # Ordenar por fecha
}

# Realizar solicitud
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    events = response.json().get("value", [])
    for event in events:
        print(f"Título: {event['subject']}")
        print(f"Inicio: {event['start']['dateTime']}")
        print(f"Fin: {event['end']['dateTime']}")
        print("---")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

{% endcode %}

#### Método 2: Filtrando con `/events`

Este método es útil cuando necesitas más control sobre los filtros. Nota que no expande eventos recurrentes automáticamente.

{% code title="A4\_2\_filter\_events.py" overflow="wrap" expandable="true" %}

```python
import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Definir rango
start_date = datetime.now(timezone.utc)
end_date = start_date + timedelta(days=30)

# Formatear fechas para el filtro
start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S')
end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S')

# Construir filtro OData
filter_query = (
    f"start/dateTime ge '{start_str}' and "
    f"start/dateTime lt '{end_str}'"
)

url = "https://graph.microsoft.com/v1.0/me/calendar/events"

params = {
    "$filter": filter_query,
    "$orderby": "start/dateTime",
    "$top": 50
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    events = response.json().get("value", [])
    print(f"Encontrados {len(events)} eventos")
else:
    print(f"Error: {response.status_code}")
```

{% endcode %}

#### 3. Manejo de Eventos Recurrentes&#x20;

#### El Problema de los Eventos Recurrentes

Los eventos recurrentes presentan un desafío:

* La API devuelve solo el evento "master" (serie principal)
* No muestra las instancias individuales dentro del rango de fechas
* Usar `/`**`events`** con filtro por fecha no captura recurrentes correctamente

#### Solución: Usar `calendarView`

{% code title="A4\_3\_get\_calendar\_events\_with\_recurring.py" overflow="wrap" expandable="true" %}

```python
import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)

def get_calendar_events_with_recurring(access_token, days_ahead=7):
    """
    Obtiene eventos incluidos los recurrentes en el rango especificado.
    calendarView maneja automáticamente la expansión de eventos recurrentes.
    """    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Prefer": "outlook.timezone=\"Europe/Madrid\""
    }
    
    start = datetime.now(timezone.utc)
    end = start + timedelta(days=days_ahead)
    
    params = {
        "startDateTime": start.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "endDateTime": end.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "$select": "subject,start,end,iCalUId,type,isReminderOn,reminderMinutesBeforeStart",
        "$orderby": "start/dateTime"
    }
    
    url = "https://graph.microsoft.com/v1.0/me/calendarView"
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# Uso
events = get_calendar_events_with_recurring(token, days_ahead=14)

for event in events:
    print(f"Evento: {event['subject']}")
    print(f"Tipo: {event['type']}")  # singleInstance, occurrence, exception, seriesMaster
    print(f"Inicio: {event['start']['dateTime']}")
```

{% endcode %}

#### Alternativa: Obtener Instancias de un Evento Recurrente

Si tienes el ID de un evento recurrente y necesitas sus instancias:

{% code title="A4\_4\_get\_recurring\_event\_instances.py" overflow="wrap" expandable="true" %}

```python
import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)

def get_recurring_event_instances(access_token, event_id, start_date, end_date):
    """
    Obtiene las instancias de un evento recurrente dentro de un rango.
    """
   
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    params = {
        "startDateTime": start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "endDateTime": end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    }
    
    url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}/instances"
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        return []

# Uso
start = datetime.now(timezone.utc)
end = start + timedelta(days=30)

instances = get_recurring_event_instances(token, "event-id-here", start, end)
for instance in instances:
    print(f"Instancia: {instance['subject']} en {instance['start']['dateTime']}")
```

{% endcode %}

#### 4. Filtros Avanzados con OData&#x20;

#### Filtros Básicos

{% code overflow="wrap" expandable="true" %}

```python
# Eventos que comienzan después de una fecha
filter1 = "start/dateTime ge '2025-01-15T09:00:00'"

# Eventos en un rango específico
filter2 = "start/dateTime ge '2025-01-15T00:00:00' and end/dateTime le '2025-01-31T23:59:59'"

# Eventos por categoría
filter3 = "categories/any(c:c eq 'Trabajo')"

# Eventos sin categoría
filter4 = "not(categories/any())"

# Eventos por organizador
filter5 = "organizer/emailAddress/address eq 'jefe@empresa.com'"

# Combinar múltiples filtros
filter_combined = (
    "start/dateTime ge '2025-01-15T00:00:00' and "
    "categories/any(c:c eq 'Importante') and "
    "isReminderOn eq true"
)
```

{% endcode %}

#### Implementación de Filtros Complejos

{% code title="A4\_5\_get\_filtered\_calendar\_events.py" overflow="wrap" expandable="true" %}

```python
import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)

def get_filtered_calendar_events(access_token, filters):
    """
    Obtiene eventos con filtros OData complejos.
    
    Args:
        filters: Diccionario con criterios de filtrado
    
    Example:
        filters = {
            'start_date': '2025-01-01T00:00:00Z',
            'end_date': '2025-01-31T23:59:59Z',
            'category': 'Trabajo',
            'is_reminder_on': True
        }
    """
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Construir filtro base por fechas
    filter_parts = []
    
    if 'start_date' in filters and 'end_date' in filters:
        filter_parts.append(
            f"start/dateTime ge '{filters['start_date']}' and "
            f"start/dateTime lt '{filters['end_date']}'"
        )
    
    if 'category' in filters:
        filter_parts.append(f"categories/any(c:c eq '{filters['category']}')")
    
    if 'is_reminder_on' in filters:
        reminder_value = str(filters['is_reminder_on']).lower()
        filter_parts.append(f"isReminderOn eq {reminder_value}")
    
    if 'subject_contains' in filters:
        filter_parts.append(
            f"startsWith(subject, '{filters['subject_contains']}')"
        )
    
    filter_query = " and ".join(filter_parts)
    
    params = {
        "$filter": filter_query,
        "$select": "subject,start,end,categories,isReminderOn",
        "$orderby": "start/dateTime"
    }
    
    url = "https://graph.microsoft.com/v1.0/me/calendar/events"
    response = requests.get(url, headers=headers, params=params)
    
    return response.json().get("value", []) if response.status_code == 200 else []

# Uso
filters = {
    'start_date': '2025-01-01T00:00:00Z',
    'end_date': '2025-01-31T23:59:59Z',
    'category': 'Trabajo',
    'is_reminder_on': True
}

events = get_filtered_calendar_events(token, filters)
```

{% endcode %}

#### 5. Manejo de Zonas Horarias&#x20;

Microsoft Graph maneja las zonas horarias automáticamente, pero es importante entender cómo configurarlas:

{% code title="A4\_6\_get\_calendar\_events\_with\_timezone.py" overflow="wrap" expandable="true" %}

```python
import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)

def get_calendar_events_with_timezone(access_token, tz="Europe/Madrid", days=7):
    """
    Obtiene eventos respetando zona horaria.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Prefer": f'outlook.timezone="{tz}"'  # Comillas dobles
    }
    
    now_utc = datetime.now(timezone.utc)
    start = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")  # 2026-02-11T10:50:00Z
    end_utc = now_utc + timedelta(days=days)
    end = end_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    params = {
        "$select": "subject,start,end,organizer",
        "$orderby": "start/dateTime"
    }
    
    url = f"https://graph.microsoft.com/v1.0/me/calendarView?startDateTime={start}&endDateTime={end}"
    
    print(f"🔍 Query: {url}")  # Debug
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        events = response.json().get("value", [])
        for event in events:
            print(f"📅 {event['subject']}")
            print(f"  Inicio: {event['start']['dateTime']} ({event['start']['timeZone']})")
            print(f"  Fin: {event['end']['dateTime']} ({event['end']['timeZone']})")
            print(f"  Organizador: {event.get('organizer', {}).get('emailAddress', {}).get('name', 'N/A')}")
            print("---")
        return events
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return []

# Test
get_calendar_events_with_timezone(token, tz="Europe/Madrid", days=7)

```

{% endcode %}

#### 6. Paginación y Rendimiento&#x20;

Para calendarios con muchos eventos, la paginación es crucial:

{% code title="A4\_7\_get\_all\_calendar\_events\_paginated.py" overflow="wrap" expandable="true" %}

```python
import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)

def get_all_calendar_events_paginated(access_token, start_date, end_date, page_size=25):
    """
    Obtiene todos los eventos con paginación automática.
    """
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    all_events = []
    skip_token = None
    
    while True:
        params = {
            "startDateTime": start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "endDateTime": end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "$top": page_size,
            "$orderby": "start/dateTime"
        }
        
        # Si hay token de paginación, úsalo
        if skip_token:
            params["$skiptoken"] = skip_token
        
        url = "https://graph.microsoft.com/v1.0/me/calendarView"
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            break
        
        data = response.json()
        all_events.extend(data.get("value", []))
        
        # Comprobar si hay más páginas
        if "@odata.nextLink" in data:
            # Extraer skiptoken del nextLink
            skip_token = data["@odata.nextLink"].split("$skiptoken=")[1]
        else:
            break
    
    return all_events

# Uso
start = datetime.now(timezone.utc)
end = start + timedelta(days=30)

all_events = get_all_calendar_events_paginated(token, start, end, page_size=25)
print(f"Total de eventos obtenidos: {len(all_events)}")
```

{% endcode %}

#### Buenas Prácticas de Rendimiento

{% code overflow="wrap" expandable="true" %}

```python
# ❌ NO HACER: Solicitar todo sin límites
bad_request = {
    "$top": 1000,  # Muy alto
}

# ✅ HACER: Paginar eficientemente
good_request = {
    "$top": 25,  # Tamaño razonable
    "$select": "subject,start,end",  # Solo campos necesarios
    "$orderby": "start/dateTime",  # Ordenamiento eficiente
}

# ✅ HACER: Usar skiptoken en lugar de skip
# skiptoken es más eficiente que $skip para grandes conjuntos
params_good = {
    "$top": 25,
    "$skiptoken": "token_value_from_nextLink"
}

# ❌ NO HACER: Usar $skip para grandes paginas
params_bad = {
    "$top": 25,
    "$skip": 10000  # Ineficiente
}
```

{% endcode %}

#### 7. Ejemplo Práctico: Sistema de Vista de Calendario&#x20;

{% code title="A4\_8\_calendar\_view\.py" overflow="wrap" expandable="true" %}

```python
from typing import List, Dict
import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)

class CalendarView:
    """
    Gestor de vistas de calendario para Microsoft 365.
    """
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://graph.microsoft.com/v1.0"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Prefer": "outlook.timezone=\"Europe/Madrid\""
        }
    
    def get_week_view(self, start_date: datetime = None) -> List[Dict]:
        """Obtiene la vista de una semana."""
        if start_date is None:
            start_date = datetime.now(timezone.utc)
        
        end_date = start_date + timedelta(days=7)
        return self._get_events_in_range(start_date, end_date)
    
    def get_month_view(self, year: int, month: int) -> List[Dict]:
        """Obtiene la vista de un mes."""
        start_date = datetime(year, month, 1)
        
        # Calcular último día del mes
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        return self._get_events_in_range(start_date, end_date)
    
    def get_today_events(self) -> List[Dict]:
        """Obtiene los eventos de hoy."""
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        return self._get_events_in_range(today, tomorrow)
       
    def _get_events_in_range(self, start: datetime, end: datetime) -> List[Dict]:
        """Obtiene eventos en un rango de fechas."""
        params = {
            "startDateTime": start.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "endDateTime": end.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "$select": "subject,start,end,categories,isReminderOn,organizer",
            "$orderby": "start/dateTime"
        }
        
        url = f"{self.base_url}/me/calendarView"
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json().get("value", [])
        else:
            raise Exception(f"Error al obtener eventos: {response.status_code}")

# Uso del sistema
calendar = CalendarView(token)

# Vista semanal
week_events = calendar.get_week_view()
print(f"Eventos esta semana: {len(week_events)}")

# Vista mensual
month_events = calendar.get_month_view(2025, 1)
print(f"Eventos en enero 2025: {len(month_events)}")

# Eventos de hoy
today_events = calendar.get_today_events()
for event in today_events:
    print(f"- {event['subject']} ({event['start']['dateTime']})")

# Estado de disponibilidad
start = datetime.now(timezone.utc)
end = start + timedelta(days=1)
events = calendar._get_events_in_range(start, end)
print(events)
```

{% endcode %}

#### Buenas Prácticas&#x20;

#### ✅ Recomendaciones

1. **Usar `calendarView` para rangos de fechas**: Siempre que necesites eventos dentro de un período específico.
2. **Especificar `$select` explícitamente**: Solo pedir los campos que necesitas para reducir tamaño de respuesta.

```python
# ✅ Eficiente
"$select": "subject,start,end"

# ❌ Innecesario
# Sin $select devuelve todos los campos
```

3. **Implementar manejo de errores robusto**:

{% code overflow="wrap" expandable="true" %}

```python
import time

def get_events_with_retry(access_token, start, end, max_retries=3):
    """Obtiene eventos con reintentos en caso de throttling."""
    for attempt in range(max_retries):
        try:
            # Realizar solicitud
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json().get("value", [])
            elif response.status_code == 429:  # Rate limit
                wait_time = int(response.headers.get('Retry-After', 60))
                print(f"Rate limited. Esperando {wait_time} segundos...")
                time.sleep(wait_time)
            else:
                raise Exception(f"Error {response.status_code}")
        
        except requests.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
    
    return []
```

{% endcode %}

4. **Validar rangos de fechas**:

{% code overflow="wrap" expandable="true" %}

```python
def validate_date_range(start: datetime, end: datetime):
    """Valida que el rango sea válido."""
    if start >= end:
        raise ValueError("start_date debe ser anterior a end_date")
    
    max_range = timedelta(days=365)
    if (end - start) > max_range:
        raise ValueError(f"Rango máximo permitido: {max_range.days} días")
    
    return True
```

{% endcode %}

#### <mark style="color:$primary;">Ejercicios</mark>&#x20;

#### <mark style="color:$primary;">Ejercicio 1: Obtener Eventos de Esta Semana</mark>

<mark style="color:$primary;">Crea una función que devuelva todos los eventos de la semana actual, ordenados por hora de inicio.</mark>

#### <mark style="color:$primary;">Ejercicio 2: Calcular Horas Disponibles</mark>

<mark style="color:$primary;">Crea una función que calcule, para esta semana, (a) Horas libres y (b) % Horas de reuniones (con mas de un asistente).</mark>

<mark style="color:$primary;">Para pasar de formato Graph a segundos, usar</mark>&#x20;

```python
datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
```

***

### Paginación y manejo de adjuntos grandes

#### 1. Fundamentos de Paginación&#x20;

#### ¿Por Qué es Necesaria la Paginación?

Imagina consultar un usuario con 10,000 correos. Devolver todos a la vez consumiría:

* Memoria excesiva
* Ancho de banda innecesario
* Tiempos de respuesta lentos
* Riesgo de timeout

La paginación **divide los resultados en páginas manejables**.

#### Conceptos Básicos

<table><thead><tr><th width="157">Parámetro</th><th>Propósito</th><th>Uso Recomendado</th></tr></thead><tbody><tr><td>$<strong>top</strong></td><td>Tamaño de página</td><td>Siempre especificar</td></tr><tr><td>$<strong>skip</strong></td><td>Saltar N resultados</td><td>Evitar para grandes volumenes</td></tr><tr><td>$<strong>skiptoken</strong></td><td>Token de paginación</td><td>Preferido, más eficiente</td></tr></tbody></table>

#### Respuestas Paginadas

Cuando hay más resultados, Microsoft Graph devuelve:

{% code overflow="wrap" expandable="true" %}

```json
{
  "value": [
    { "id": "1", "subject": "Email 1" },
    { "id": "2", "subject": "Email 2" }
  ],
  "@odata.nextLink": "https://graph.microsoft.com/v1.0/me/messages?$top=2&$skiptoken=RFNwdA..."
}
```

{% endcode %}

**Nunca** extraigas el `$skiptoken` manualmente. Usa siempre la URL completa del `@odata.nextLink`.

#### Límites de Página por API

| API                       | Por Defecto | Máximo | Soporta $skip |
| ------------------------- | ----------- | ------ | ------------- |
| **`/me/messages`**        | 10          | 1000   | Sí            |
| **`/users`**              | 100         | 999    | No            |
| **`/me/mailFolders`**     | 10          | 1000   | Sí            |
| **`/groups`**             | 100         | N/A    | No            |
| **`/me/calendar/events`** | 25          | 1000   | Sí            |

#### 2. Implementación de Paginación Correcta

#### Patrón Recomendado: Usando @odata.nextLink

{% code title="A5\_1\_get\_all\_messages\_paginated.py" overflow="wrap" expandable="true" %}

```python
from typing import List, Dict
import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Mail.Read"]
token = get_delegated_token(SCOPES)

def get_all_messages_paginated(access_token, top=25):
    """
    Inbox directo SIN folder ID.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    
    all_messages = []
    url = "https://graph.microsoft.com/v1.0/me/messages"  # ← Inbox default
    
    params = {"$top": top, "$select": "subject,from,receivedDateTime"}
    
    while url and len(all_messages) < 1000:  # Límite razonable
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"❌ Error {response.status_code}: {response.text}")
            break
        
        data = response.json()
        all_messages.extend(data.get("value", []))
        
        url = data.get("@odata.nextLink")
        params = {}  # NextLink ya tiene todo
        
        print(f"📥 {len(data['value'])} msgs. Total: {len(all_messages)}")
    
    return all_messages

# Uso
messages = get_all_messages_paginated(token)
print(f"Total de mensajes: {len(messages)}")
```

{% endcode %}

#### ❌ Antipatrón: Extrayendo $skiptoken

{% code overflow="wrap" expandable="true" %}

```python
# NUNCA hagas esto:
next_link = data["@odata.nextLink"]
skiptoken = next_link.split("$skiptoken=")[1]  # ❌ INCORRECTO

# Siempre usa la URL completa
next_url = data["@odata.nextLink"]  # ✅ CORRECTO
```

{% endcode %}

#### ⚠️ Limitaciones de $skip

```python
# PROBLEMA: En consultas grandes, $skip es ineficiente
# Ejemplo de rendimiento:
# - $skip=0: 10ms
# - $skip=1000: 50ms
# - $skip=10000: 200ms
# - $skip=100000: 2000ms (2 segundos)

# SOLUCIÓN: Usa siempre $skiptoken cuando esté disponible
```

#### 3. Manejo de Errores en Paginación&#x20;

#### Errores Comunes y Soluciones

{% code overflow="wrap" expandable="true" %}

```python
def get_items_with_error_handling(access_token, max_retries=3):
    """Paginación con manejo robusto de errores."""
    import time
    
    headers = {"Authorization": f"Bearer {access_token}"}
    all_items = []
    url = "https://graph.microsoft.com/v1.0/me/messages"
    
    params = {"$top": 25}
    retry_count = 0
    last_successful_url = None
    
    while url:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            # Rate limit (429)
            if response.status_code == 429:
                wait_time = int(response.headers.get('Retry-After', 60))
                print(f"Rate limited. Esperando {wait_time}s...")
                time.sleep(wait_time)
                continue
            
            # Token expirado (401)
            if response.status_code == 401:
                print("Token expirado. Necesita renovación.")
                break
            
            # Error permanente
            if response.status_code >= 400:
                print(f"Error {response.status_code}: {response.text}")
                break
            
            # Éxito
            data = response.json()
            all_items.extend(data.get("value", []))
            last_successful_url = url
            
            # Token especial: DirectoryPageTokenNotFoundException
            # Guardar el último token exitoso
            url = data.get("@odata.nextLink", None)
            params = {}
            retry_count = 0
        
        except requests.Timeout:
            retry_count += 1
            if retry_count < max_retries:
                print(f"Timeout. Reintentando ({retry_count}/{max_retries})...")
                time.sleep(2 ** retry_count)
                # Reintentar con la misma URL
                continue
            else:
                print("Máximo de reintentos alcanzado.")
                break
        
        except Exception as e:
            print(f"Error inesperado: {e}")
            break
    
    return all_items

# Uso
items = get_items_with_error_handling(token)
```

{% endcode %}

#### 4. Adjuntos Pequeños vs Grandes&#x20;

#### Estrategia por Tamaño

```
Tamaño      │ Estrategia              │ Método
────────────┼─────────────────────────┼─────────────────────
< 3 MB      │ Directo (simple)        │ POST a /attachments
3-150 MB    │ Upload session (chunked)│ createUploadSession + PUT
> 150 MB    │ No soportado            │ Usar OneDrive como alternativa
```

#### Adjuntos Pequeños: Método Simple

{% code title="A5\_2\_attach\_small\_file.py" overflow="wrap" expandable="true" %}

```python
import base64
import requests
from A0_1_get_token import get_delegated_token

SCOPES = ["Mail.ReadWrite"]
token = get_delegated_token(SCOPES)

def attach_small_file(access_token, message_id, file_path):
    """
    Adjunta un archivo pequeño (< 3 MB) directamente.
    Método simple y rápido.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Leer archivo
    with open(file_path, "rb") as f:
        file_content = f.read()
    
    # Convertir a base64
    content_base64 = base64.b64encode(file_content).decode()
    
    # Preparar payload
    attachment = {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": "documento.pdf",
        "contentBytes": content_base64
    }
    
    # Enviar
    url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments"
    response = requests.post(url, headers=headers, json=attachment)
    
    if response.status_code == 201:
        attachment_id = response.json().get("id")
        print(f"Archivo adjuntado: {attachment_id}")
        return True
    else:
        print(f"Error: {response.status_code}")
        return False

# Uso
attach_small_file(token, "message-id-here", "documento.pdf")
```

{% endcode %}

#### Validar Tamaño Antes de Comenzar

{% code overflow="wrap" expandable="true" %}

```python
import os

def validate_attachment_size(file_path, max_size_mb=150):
    """Valida que el archivo sea adjuntable."""
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    
    if file_size_mb > max_size_mb:
        raise ValueError(f"Archivo demasiado grande: {file_size_mb:.1f}MB (máx: {max_size_mb}MB)")
    
    return file_size_bytes

# Uso
try:
    size = validate_attachment_size("video.mp4")
    print(f"Tamaño validado: {size} bytes")
except ValueError as e:
    print(f"Error: {e}")
```

{% endcode %}

#### 5. Upload Sessions para Adjuntos Grandes&#x20;

#### Proceso de 3 Pasos

```
Paso 1: Crear Upload Session
   └─ POST /messages/{id}/attachments/createUploadSession
   └─ Recibe: uploadUrl, expirationDateTime

Paso 2: Subir Chunks (hasta 4 MB cada uno)
   └─ PUT {uploadUrl}/content
   └─ Headers: Content-Range, Content-Length
   └─ Repetir hasta subir todo

Paso 3: Completar Upload
   └─ Automático cuando se completa último chunk
```

#### Implementación Completa

{% code title="A5\_3\_large\_attachment\_uploader.py" overflow="wrap" expandable="true" %}

```python
from pathlib import Path
import requests
from A0_1_get_token import get_delegated_token

SCOPES = ["Mail.ReadWrite"]
token = get_delegated_token(SCOPES)

class LargeAttachmentUploader:
    """Sube adjuntos grandes (3-150 MB) a Outlook."""
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        self.chunk_size = 4 * 1024 * 1024  # 4 MB máximo
    
    def create_upload_session(self, message_id, file_path):
        """Paso 1: Crear sesión de upload."""
        file_size = Path(file_path).stat().st_size
        file_name = Path(file_path).name
        
        payload = {
            "AttachmentItem": {
                "attachmentType": "file",
                "name": file_name,
                "size": file_size
            }
        }
        
        url = f"https://graph.microsoft.com/beta/me/messages/{message_id}/attachments/createUploadSession"
        
        response = requests.post(url, headers=self.base_headers, json=payload)
        
        if response.status_code != 201:
            raise Exception(f"Error creando sesión: {response.status_code} - {response.text}")
        
        session_data = response.json()
        return {
            "uploadUrl": session_data["uploadUrl"],
            "expirationDateTime": session_data["expirationDateTime"],
            "fileSize": file_size
        }
    
    def upload_chunks(self, upload_session, file_path, on_progress=None):
        """Paso 2: Subir chunks."""
        upload_url = upload_session["uploadUrl"]
        file_size = upload_session["fileSize"]
        uploaded = 0
        
        with open(file_path, "rb") as f:
            while uploaded < file_size:
                # Leer chunk
                chunk_data = f.read(self.chunk_size)
                chunk_length = len(chunk_data)
                
                # Preparar headers para este chunk
                headers = {
                    "Content-Type": "application/octet-stream",
                    "Content-Length": str(chunk_length),
                    "Content-Range": f"bytes {uploaded}-{uploaded + chunk_length - 1}/{file_size}"
                }
                
                # Subir chunk
                response = requests.put(upload_url, headers=headers, data=chunk_data)
                
                if response.status_code not in [200, 201]:
                    raise Exception(f"Error en chunk: {response.status_code}")
                
                uploaded += chunk_length
                
                # Callback de progreso
                if on_progress:
                    percentage = (uploaded / file_size) * 100
                    on_progress(percentage, uploaded, file_size)
    
    def upload_large_attachment(self, message_id, file_path):
        """Flujo completo de upload."""
        print(f"Iniciando upload de {Path(file_path).name}...")
        
        # Paso 1: Crear sesión
        session = self.create_upload_session(message_id, file_path)
        print(f"Sesión creada. Tamaño: {session['fileSize'] / (1024*1024):.1f}MB")
        
        # Paso 2: Subir chunks
        def progress_callback(percent, uploaded, total):
            mb_uploaded = uploaded / (1024 * 1024)
            mb_total = total / (1024 * 1024)
            print(f"Progreso: {percent:.1f}% ({mb_uploaded:.1f}MB / {mb_total:.1f}MB)")
        
        self.upload_chunks(session, file_path, on_progress=progress_callback)
        
        print("Upload completado!")
        return True

# Uso
uploader = LargeAttachmentUploader(token)
uploader.upload_large_attachment("message-id", "archivo_grande.zip")
```

{% endcode %}

#### 6. Descargas de Archivos Grandes&#x20;

#### El Problema de Descargar Todo en Memoria

```python
# ❌ MAL: Carga todo en memoria
response = requests.get(file_url)
content = response.content  # Problema si archivo es grande
```

#### Solución: Descargar en Chunks

{% code title="A5\_4\_download\_file\_in\_chunks.py" overflow="wrap" expandable="true" %}

```python
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
```

{% endcode %}

#### Con Range Header para Descargas Reanudables

{% code overflow="wrap" expandable="true" %}

```python
def download_file_resumable(file_url, output_path, chunk_size=1024*1024):
    """Descarga con soporte para reanudar."""
    import os
    
    # Obtener tamaño total
    response = requests.head(file_url)
    total_size = int(response.headers.get('content-length', 0))
    
    # Si existe parcial, continuar
    if os.path.exists(output_path):
        downloaded = os.path.getsize(output_path)
    else:
        downloaded = 0
    
    with open(output_path, 'ab') as f:
        while downloaded < total_size:
            # Calcular rango
            end = min(downloaded + chunk_size, total_size) - 1
            
            headers = {
                "Range": f"bytes={downloaded}-{end}"
            }
            
            response = requests.get(file_url, headers=headers, stream=True)
            
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
            
            percent = (downloaded / total_size) * 100
            print(f"Progreso: {percent:.1f}%")
    
    print("Descarga completada")

# Uso
download_file_resumable(download_url, "archivo.bin")
```

{% endcode %}

#### 7. Buenas Prácticas y Optimizaciones&#x20;

#### ✅ Recomendaciones

**Paginación:**

* Siempre especificar `$top` (25-50 es buena opción)
* Usar `@odata.nextLink` completo (no extraer skiptoken)
* Guardar último token exitoso para reintentos
* Implementar timeout (10-30 segundos)

**Adjuntos:**

* Validar tamaño antes de comenzar
* Usar 4 MB como tamaño de chunk máximo
* Implementar callbacks de progreso
* Reutilizar upload sessions si es posible

{% code overflow="wrap" expandable="true" %}

```python
# Configuración recomendada
CONFIG = {
    "pagination": {
        "page_size": 25,
        "timeout": 30,
        "max_retries": 3
    },
    "attachments": {
        "chunk_size": 4 * 1024 * 1024,  # 4 MB
        "max_size": 150 * 1024 * 1024,  # 150 MB
        "small_threshold": 3 * 1024 * 1024  # 3 MB
    }
}
```

{% endcode %}

#### 📊 Ejemplo Optimizado Completo

{% code overflow="wrap" expandable="true" %}

```python
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptimizedGraphClient:
    """Cliente Graph optimizado con paginación y uploads."""
    
    def __init__(self, access_token, config=None):
        self.access_token = access_token
        self.config = config or self._default_config()
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        })
    
    @staticmethod
    def _default_config():
        return {
            "page_size": 25,
            "chunk_size": 4 * 1024 * 1024,
            "timeout": 30,
            "max_retries": 3
        }
    
    def get_paginated_data(self, endpoint, **params):
        """Obtiene datos paginados con manejo completo."""
        params.setdefault("$top", self.config["page_size"])
        
        all_data = []
        url = f"https://graph.microsoft.com/v1.0{endpoint}"
        
        while url:
            try:
                response = self.session.get(url, params=params, timeout=self.config["timeout"])
                
                if response.status_code == 429:
                    wait = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Esperando {wait}s...")
                    time.sleep(wait)
                    continue
                
                response.raise_for_status()
                data = response.json()
                all_data.extend(data.get("value", []))
                
                url = data.get("@odata.nextLink", None)
                params = {}  # Ya incluido en nextLink
                
                logger.info(f"Página obtenida. Total: {len(all_data)}")
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Error: {e}")
                break
        
        return all_data
    
    def upload_attachment(self, message_id, file_path):
        """Sube anexo con tamaño automático."""
        import os
        from pathlib import Path
        
        file_size = os.path.getsize(file_path)
        
        if file_size < 3 * 1024 * 1024:
            return self._upload_small_attachment(message_id, file_path)
        else:
            return self._upload_large_attachment(message_id, file_path)
    
    def _upload_small_attachment(self, message_id, file_path):
        """Upload directo para archivos pequeños."""
        import base64
        
        with open(file_path, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        
        payload = {
            "@odata.type": "#microsoft.graph.fileAttachment",
            "name": Path(file_path).name,
            "contentBytes": content
        }
        
        url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments"
        response = self.session.post(url, json=payload)
        
        return response.status_code == 201
    
    def _upload_large_attachment(self, message_id, file_path):
        """Upload con chunks para archivos grandes."""
        # ... (ver implementación anterior)
        pass
```

{% endcode %}

#### 8. Ejemplo Práctico Integrado&#x20;

{% code overflow="wrap" expandable="true" %}

```python
# Caso de uso: Procesar y descargar adjuntos de carpeta
def process_folder_attachments(access_token, folder_id):
    """
    1. Pagina por todos los mensajes de una carpeta
    2. Extrae información de adjuntos
    3. Descarga adjuntos grandes
    """
    from pathlib import Path
    
    client = OptimizedGraphClient(access_token)
    
    # Paso 1: Obtener todos los mensajes
    endpoint = f"/me/mailFolders/{folder_id}/messages"
    messages = client.get_paginated_data(
        endpoint,
        **{"$select": "id,subject,hasAttachments,size"}
    )
    
    print(f"Total de mensajes: {len(messages)}")
    
    # Paso 2: Para cada mensaje, procesar adjuntos
    for message in messages:
        if not message.get("hasAttachments"):
            continue
        
        msg_id = message["id"]
        subject = message["subject"]
        
        # Obtener adjuntos
        attachments_endpoint = f"/me/messages/{msg_id}/attachments"
        attachments = client.get_paginated_data(attachments_endpoint)
        
        print(f"\nMensaje: {subject}")
        print(f"Adjuntos: {len(attachments)}")
        
        for att in attachments:
            name = att.get("name", "sin_nombre")
            size_mb = att.get("size", 0) / (1024 * 1024)
            
            print(f"  - {name}: {size_mb:.1f}MB")
            
            # Descargar si es pequeño
            if size_mb < 10:
                download_url = att.get("@odata.type") == "#microsoft.graph.fileAttachment"
                # ... descargar ...
```

{% endcode %}

#### <mark style="color:$primary;">Ejercicios</mark>&#x20;

#### <mark style="color:$primary;">Ejercicio 1: Paginar Mensajes</mark>

<mark style="color:$primary;">Crea una función que obtenga todos los mensajes de la bandeja de entrada mostrando asunto y numero de adjuntos.</mark>

#### <mark style="color:$primary;">Ejercicio 2: Subir Adjunto Pequeño</mark>

<mark style="color:$primary;">Crea una función que pida el nombre de un PDF pequeño y lo envie adjunto.</mark>

#### <mark style="color:$primary;">Ejercicio 3: Descargar Adjunto con Progreso</mark>

<mark style="color:$primary;">Descarga un adjunto mostrando progreso de descarga.</mark>

***

### Escenarios de automatización: recordatorios y resúmenes diarios

#### 1. Fundamentos de Automatización en Microsoft 365&#x20;

#### Opciones de Automatización

```
Opción           │ Complejidad │ Costo    │ Mejor Para
─────────────────┼─────────────┼──────────┼─────────────────────────
Power Automate   │ Baja        │ Incluido │ Flujos simples sin código
Azure Functions  │ Media       │ Bajo     │ Lógica compleja, escalable
Azure Automation │ Media       │ Bajo     │ Scripts repetitivos
Python + APSched │ Baja/Media  │ Gratis   │ Scripts locales/servidor
Logic Apps       │ Media       │ Medio    │ Integraciones empresariales
```

#### Arquitectura Básica

```
┌─────────────────┐
│   Scheduler     │  (Trigger cada día a las 9 AM)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Script Python  │  (Lógica de negocio)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Microsoft Graph │  (Obtener datos)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Enviar Email   │  (Notificar usuarios)
└─────────────────┘
```

#### Casos de Uso Comunes

<table><thead><tr><th>Caso de Uso</th><th width="188">Frecuencia</th><th>Beneficio</th></tr></thead><tbody><tr><td><strong>Recordatorio de reuniones</strong></td><td>30 min antes</td><td>No olvidas reuniones</td></tr><tr><td><strong>Resumen diario</strong></td><td>8 AM</td><td>Planificación mejor</td></tr><tr><td><strong>Reporte de tareas vencidas</strong></td><td>Diario</td><td>Control de proyectos</td></tr><tr><td><strong>Notificación de cumpleaños</strong></td><td>Trimestral</td><td>Reconocimiento del equipo</td></tr><tr><td><strong>Limpieza de calendarios</strong></td><td>Semanal</td><td>Calendario organizado</td></tr></tbody></table>

#### 2. Recordatorios Automáticos de Eventos

#### El Reto

Los usuarios a menudo olvidan reuniones. Queremos enviar un email de recordatorio 30 minutos antes.

#### Solución: Script de Recordatorio

{% code title="A6\_1\_event\_reminder.py" overflow="wrap" expandable="true" %}

```python
from datetime import datetime, timedelta, timezone
import schedule # pip install schedule
import time
import requests
from A0_1_get_token import get_delegated_token

class EventReminder:
    """Sistema automático de recordatorios de eventos."""
    
    def __init__(self, access_token, user_email):
        self.access_token = access_token
        self.user_email = user_email
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def get_upcoming_events(self, minutes_ahead=40):
        """Obtiene eventos en los próximos N minutos."""
        now = datetime.now(timezone.utc)
        future = now + timedelta(minutes=minutes_ahead)
        
        params = {
            "startDateTime": now.isoformat() + "Z",
            "endDateTime": future.isoformat() + "Z",
            "$select": "subject,start,end,attendees,onlineMeetingUrl,organizer",
            "$orderby": "start/dateTime"
        }
        
        url = "https://graph.microsoft.com/v1.0/me/calendarView"
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json().get("value", [])
        else:
            print(f"Error: {response.status_code}")
            return []
    
    def should_send_reminder(self, event):
        """Verifica si debe enviar recordatorio (30 min antes)."""
        event_time = datetime.fromisoformat(
            event["start"]["dateTime"].replace("Z", "+00:00")
        )
        now = datetime.utcnow().replace(tzinfo=event_time.tzinfo)
        
        minutes_until = (event_time - now).total_seconds() / 60
        
        # Enviar recordatorio entre 31 y 29 minutos antes
        return 29 <= minutes_until <= 31
    
    def send_reminder_email(self, event):
        """Envía email de recordatorio del evento."""
        event_time = event["start"]["dateTime"]
        subject = event["subject"]
        organizer = event.get("organizer", {}).get("emailAddress", {}).get("name", "Unknown")
        attendees_count = len(event.get("attendees", []))
        meeting_url = event.get("onlineMeetingUrl", "No disponible")
        
        # Generar HTML del email
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Recordatorio de Reunión</h2>
                <p><b>Título:</b> {subject}</p>
                <p><b>Hora:</b> {event_time}</p>
                <p><b>Organizador:</b> {organizer}</p>
                <p><b>Asistentes:</b> {attendees_count}</p>
                <hr>
                <p><b>Enlace de reunión:</b> <a href="{meeting_url}">{meeting_url}</a></p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    Este es un recordatorio automático de su sistema de automatización.
                </p>
            </body>
        </html>
        """
        
        payload = {
            "message": {
                "subject": f"Recordatorio: {subject} en 30 minutos",
                "body": {
                    "contentType": "HTML",
                    "content": html_body
                },
                "toRecipients": [
                    {"emailAddress": {"address": self.user_email}}
                ]
            },
            "saveToSentItems": True
        }
        
        url = "https://graph.microsoft.com/v1.0/me/sendMail"
        response = requests.post(url, headers=self.headers, json=payload)
        
        return response.status_code == 202
    
    def process_reminders(self):
        """Procesa todos los recordatorios pendientes."""
        events = self.get_upcoming_events()
        
        print(f"Verificando {len(events)} eventos próximos...")
        
        sent_count = 0
        for event in events:
            if self.should_send_reminder(event):
                subject = event["subject"]
                if self.send_reminder_email(event):
                    print(f"✓ Recordatorio enviado: {subject}")
                    sent_count += 1
                else:
                    print(f"✗ Error enviando recordatorio: {subject}")
        
        return sent_count

if __name__ == "__main__":
    SCOPES = ["Mail.ReadWrite"]
    token = get_delegated_token(SCOPES)

    # Uso
    reminder = EventReminder(token, "user@empresa.com")

    # Ejecutar cada 5 minutos
    schedule.every(5).minutes.do(reminder.process_reminders)

    while True:
        schedule.run_pending()
        time.sleep(60)
```

{% endcode %}

#### Configuración de Scheduler

{% code overflow="wrap" expandable="true" %}

```python
# Usando APScheduler para produccción
from apscheduler.schedulers.background import BackgroundScheduler # pip install apscheduler
import atexit

def start_reminder_scheduler(access_token, user_email):
    """Inicia el scheduler de recordatorios en background."""
    reminder = EventReminder(access_token, user_email)
    
    scheduler = BackgroundScheduler()
    
    # Ejecutar cada 5 minutos
    scheduler.add_job(
        func=reminder.process_reminders,
        trigger="interval",
        minutes=5,
        id="event_reminders"
    )
    
    scheduler.start()
    
    # Limpiar al cerrar
    atexit.register(lambda: scheduler.shutdown())
    
    print("✓ Scheduler de recordatorios iniciado")
    return scheduler
```

{% endcode %}

#### 3. Resúmenes Diarios Personalizados&#x20;

#### Concepto

Cada mañana a las 8 AM, enviar un resumen con:

* Reuniones de hoy
* Tareas vencidas de Planner
* Correos importantes sin leer
* Próximos cumpleaños

#### Implementación Completa

{% code title="A6\_2\_daily\_summary.py" overflow="wrap" expandable="true" %}

```python
from datetime import datetime, timezone
from jinja2 import Template # pip install jinja2
import requests
from apscheduler.schedulers.background import BackgroundScheduler

class DailySummaryGenerator:
    """Genera resúmenes diarios personalizados."""
    
    def __init__(self, access_token, user_email):
        self.access_token = access_token
        self.user_email = user_email
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def get_today_events(self):
        """Obtiene reuniones de hoy."""
        today = datetime.now(timezone.utc).date()
        start = datetime(today.year, today.month, today.day, 0, 0, 0).isoformat() + "Z"
        end = datetime(today.year, today.month, today.day, 23, 59, 59).isoformat() + "Z"
        
        params = {
            "startDateTime": start,
            "endDateTime": end,
            "$select": "subject,start,end,isReminderOn,organizer",
            "$orderby": "start/dateTime"
        }
        
        url = "https://graph.microsoft.com/v1.0/me/calendarView"
        response = requests.get(url, headers=self.headers, params=params)
        
        return response.json().get("value", []) if response.status_code == 200 else []
    
    def get_overdue_tasks(self):
        """Obtiene tareas vencidas de Planner."""
        # Asumir que tenemos plan_id conocido
        # En producción, obtener desde configuración
        
        today = datetime.now(timezone.utc).date().isoformat()
        
        params = {
            "$filter": f"dueDateTime lt '{today}'",
            "$select": "title,dueDateTime,percentComplete,assignments"
        }
        
        url = "https://graph.microsoft.com/v1.0/me/planner/tasks"
        response = requests.get(url, headers=self.headers, params=params)
        
        return response.json().get("value", []) if response.status_code == 200 else []
    
    def get_unread_emails(self):
        """Obtiene correos importantes sin leer."""
        params = {
            "$filter": "isRead eq false and importance eq 'high'",
            "$select": "subject,from,receivedDateTime,bodyPreview",
            "$orderby": "receivedDateTime desc",
            "$top": 5
        }
        
        url = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages"
        response = requests.get(url, headers=self.headers, params=params)
        
        return response.json().get("value", []) if response.status_code == 200 else []
    
    def generate_html_summary(self):
        """Genera HTML del resumen diario."""
        events = self.get_today_events()
        tasks = self.get_overdue_tasks()
        emails = self.get_unread_emails()
        
        # Template HTML
        template_str = """
        <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; background: #f5f5f5; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
                    h1 { color: #0078d4; border-bottom: 3px solid #0078d4; padding-bottom: 10px; }
                    h2 { color: #333; margin-top: 25px; font-size: 18px; }
                    .section { margin-bottom: 25px; }
                    .event-item, .task-item, .email-item { 
                        padding: 12px; 
                        border-left: 4px solid #0078d4; 
                        background: #f9f9f9; 
                        margin-bottom: 10px; 
                    }
                    .event-item { border-left-color: #107c10; }
                    .task-item { border-left-color: #ff8c00; }
                    .email-item { border-left-color: #0078d4; }
                    .time { color: #666; font-size: 12px; }
                    .empty { color: #999; font-style: italic; }
                    .footer { color: #666; font-size: 12px; text-align: center; margin-top: 30px; padding-top: 15px; border-top: 1px solid #ddd; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Resumen Diario - {{ date }}</h1>
                    
                    <div class="section">
                        <h2>Reuniones de Hoy ({{ events_count }})</h2>
                        {% if events %}
                            {% for event in events %}
                                <div class="event-item">
                                    <b>{{ event.subject }}</b>
                                    <div class="time">{{ event.start_time }} - {{ event.end_time }}</div>
                                </div>
                            {% endfor %}
                        {% else %}
                            <p class="empty">Sin reuniones programadas hoy</p>
                        {% endif %}
                    </div>
                    
                    <div class="section">
                        <h2>Tareas Vencidas ({{ tasks_count }})</h2>
                        {% if tasks %}
                            {% for task in tasks %}
                                <div class="task-item">
                                    <b>{{ task.title }}</b>
                                    <div class="time">Vencida: {{ task.due_date }}</div>
                                </div>
                            {% endfor %}
                        {% else %}
                            <p class="empty">Sin tareas vencidas</p>
                        {% endif %}
                    </div>
                    
                    <div class="section">
                        <h2>Correos Importantes sin Leer ({{ emails_count }})</h2>
                        {% if emails %}
                            {% for email in emails %}
                                <div class="email-item">
                                    <b>{{ email.subject }}</b>
                                    <div class="time">De: {{ email.from_address }} | {{ email.received_date }}</div>
                                    <p>{{ email.preview }}</p>
                                </div>
                            {% endfor %}
                        {% else %}
                            <p class="empty">Sin correos pendientes</p>
                        {% endif %}
                    </div>
                    
                    <div class="footer">
                        <p>Este resumen fue generado automáticamente a las {{ generation_time }}</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Preparar datos
        template_data = {
            "date": datetime.now().strftime("%d de %B de %Y"),
            "events": [{
                "subject": e["subject"],
                "start_time": e["start"]["dateTime"].split("T")[1][:5],
                "end_time": e["end"]["dateTime"].split("T")[1][:5]
            } for e in events],
            "events_count": len(events),
            "tasks": [{
                "title": t["title"],
                "due_date": t.get("dueDateTime", "N/A")
            } for t in tasks],
            "tasks_count": len(tasks),
            "emails": [{
                "subject": em["subject"],
                "from_address": em["from"]["emailAddress"]["name"],
                "received_date": em["receivedDateTime"][:10],
                "preview": em["bodyPreview"][:100]
            } for em in emails],
            "emails_count": len(emails),
            "generation_time": datetime.now().strftime("%H:%M:%S")
        }
        
        template = Template(template_str)
        return template.render(**template_data)
    
    def send_summary(self):
        """Envía el resumen diario por email."""
        html_content = self.generate_html_summary()
        
        payload = {
            "message": {
                "subject": f"Tu Resumen Diario - {datetime.now().strftime('%d %B %Y')}",
                "body": {
                    "contentType": "HTML",
                    "content": html_content
                },
                "toRecipients": [
                    {"emailAddress": {"address": self.user_email}}
                ]
            },
            "saveToSentItems": True
        }
        
        url = "https://graph.microsoft.com/v1.0/me/sendMail"
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 202:
            print("✓ Resumen diario enviado")
            return True
        else:
            print(f"✗ Error enviando resumen: {response.status_code}")
            return False

# Uso con scheduler
def schedule_daily_summary(access_token, user_email, hour=8, minute=0):
    """Programa el resumen diario."""
    
    summary = DailySummaryGenerator(access_token, user_email)
    scheduler = BackgroundScheduler()
    
    # Ejecutar cada día a la hora especificada
    scheduler.add_job(
        func=summary.send_summary,
        trigger="cron",
        hour=hour,
        minute=minute,
        id="daily_summary"
    )
    
    scheduler.start()
    print(f"✓ Resumen diario programado para las {hour:02d}:{minute:02d}")
```

{% endcode %}

#### 4. Buenas Prácticas de Automatización&#x20;

#### ✅ Recomendaciones Clave

{% code overflow="wrap" expandable="true" %}

```python
# 1. Usar Variables de Entorno
import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("GRAPH_ACCESS_TOKEN")
USER_EMAIL = os.getenv("USER_EMAIL")

# 2. Implementar Logging Detallado
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 3. Manejo de Errores Robusto
try:
    reminder.process_reminders()
except requests.Timeout:
    logger.error("Timeout en API Graph")
except Exception as e:
    logger.error(f"Error inesperado: {e}")

# 4. Monitorear Ejecución
def log_execution(func):
    """Decorator para loguear ejecuciones."""
    def wrapper(*args, **kwargs):
        start = datetime.now()
        logger.info(f"Iniciando: {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            elapsed = (datetime.now() - start).total_seconds()
            logger.info(f"Completado: {func.__name__} en {elapsed:.2f}s")
            return result
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {e}")
            raise
    
    return wrapper

@log_execution
def my_automation_task():
    pass

# 5. Notificar Problemas
def send_error_notification(error_message):
    """Notifica si hay error en la automatización."""
    payload = {
        "message": {
            "subject": "⚠️ Error en Automatización",
            "body": {
                "contentType": "text",
                "content": f"Error: {error_message}"
            },
            "toRecipients": [
                {"emailAddress": {"address": "admin@empresa.com"}}
            ]
        }
    }
    # Enviar...
```

{% endcode %}

#### ⚠️ Anti-patrones a Evitar

{% code overflow="wrap" expandable="true" %}

```python
# ❌ NO HACER: Hardcoding de credenciales
ACCESS_TOKEN = "eyJ0eXAi..."  # ¡Nunca!

# ❌ NO HACER: Sin manejo de errores
events = requests.get(url).json()["value"]  # Puede fallar

# ❌ NO HACER: Sin logging
result = my_function()  # ¿Qué pasó?

# ❌ NO HACER: Reintentos infinitos
while True:
    requests.get(url)  # Se queda atrapado

# ✅ HACER: Token de variables de entorno
ACCESS_TOKEN = os.getenv("GRAPH_TOKEN")

# ✅ HACER: Manejo completo de errores
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    logger.error(f"Error: {e}")

# ✅ HACER: Logging informativo
logger.info(f"Procesando {len(items)} items")

# ✅ HACER: Reintentos con backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def get_data():
    return requests.get(url).json()
```

{% endcode %}

#### 5. Ejemplo Práctico Integrado&#x20;

{% code title="A6\_3\_automation.py - Solución completa de automatización" overflow="wrap" expandable="true" %}

```python
import logging
import os
import schedule
import time
from dotenv import load_dotenv
from A0_1_get_token import get_delegated_token
from A6_2_daily_summary import DailySummaryGenerator
from A6_1_event_reminder import EventReminder

# Configuración
SCOPES = ["Mail.ReadWrite"]
token = get_delegated_token(SCOPES)
USER_EMAIL = os.getenv("USER_EMAIL")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutomationEngine:
    """Motor central de automatización."""
    
    def __init__(self, token, email):
        self.token = token
        self.email = email
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.tasks = []
    
    def add_task(self, name, func, schedule_config):
        """Registra una tarea automática."""
        self.tasks.append({
            "name": name,
            "func": func,
            "schedule": schedule_config
        })
    
    def start(self):
        """Inicia el motor de automatización."""
        for task in self.tasks:
            name = task["name"]
            config = task["schedule"]
            
            if config["type"] == "interval":
                schedule.every(config["minutes"]).minutes.do(task["func"])
                logger.info(f"Tarea '{name}' programada cada {config['minutes']} minutos")
            
            elif config["type"] == "daily":
                schedule.every().day.at(config["time"]).do(task["func"])
                logger.info(f"Tarea '{name}' programada diariamente a las {config['time']}")
        
        logger.info("=== MOTOR DE AUTOMATIZACIÓN INICIADO ===")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

# Instanciar motor
engine = AutomationEngine(token, USER_EMAIL)

# Registrar tareas
reminder = EventReminder(token, USER_EMAIL)
engine.add_task(
    name="Recordatorios de eventos",
    func=reminder.process_reminders,
    schedule_config={"type": "interval", "minutes": 5}
)

summary = DailySummaryGenerator(token, USER_EMAIL)
engine.add_task(
    name="Resumen diario",
    func=summary.send_summary,
    schedule_config={"type": "daily", "time": "08:00"}
)

# Iniciar
if __name__ == "__main__":
    engine.start()
```

{% endcode %}

#### <mark style="color:$primary;">Ejercicio: Inbox Cero</mark>

<mark style="color:$primary;">Crea una automatización que, a medio dia:</mark>

* <mark style="color:$primary;">Liste los correos importantes sin abrir</mark>
* <mark style="color:$primary;">Cree un evento al final de la jornada para contestarlos. 5 minutos por correo.</mark>

***

### Integración con To-Dos: correo → tarea o evento → tarea

#### 1. Arquitectura de Integración&#x20;

#### Flujo General

```
Correo/Evento
    ↓
Validación
    ↓
Extracción de datos
    ↓
Creación de To-Do
    ↓
Asignación
    ↓
Auditoría
```

#### API Graph de To-Do <a href="#endpoints-principales" id="endpoints-principales"></a>

Requiere scopes `Tasks.ReadWrite` (delegado)

Base: `https://graph.microsoft.com/v1.0/me/todo`

#### Listas (todoTaskLists)

<table><thead><tr><th width="142">Acción</th><th>Endpoint</th><th>Ejemplo</th></tr></thead><tbody><tr><td>Listar</td><td><code>GET /me/todo/lists</code></td><td><code>?$filter=displayName eq 'Trabajo'</code></td></tr><tr><td>Crear</td><td><code>POST /me/todo/lists</code></td><td><code>{"displayName": "Compras"}</code></td></tr><tr><td>Detalle</td><td><code>GET /me/todo/lists/{listId}</code></td><td>-</td></tr><tr><td>Eliminar</td><td><code>DELETE /me/todo/lists/{listId}</code></td><td>-</td></tr><tr><td>Actualizar</td><td><code>PATCH /me/todo/lists/{listId}</code></td><td><code>{"displayName": "Nueva"}</code> </td></tr></tbody></table>

#### Tasks (por Lista)

<table><thead><tr><th width="120">Acción</th><th width="402">Endpoint</th><th>Parámetros Clave</th></tr></thead><tbody><tr><td><strong>Listar</strong></td><td><code>GET /me/todo/lists/{listId}/tasks</code></td><td><code>?$filter=status eq 'notStarted'&#x26;$orderby=dueDateTime</code><br><code>?$expand=linkedResources,checklistItems</code></td></tr><tr><td><strong>Crear</strong></td><td><code>POST /me/todo/lists/{listId}/tasks</code></td><td><code>title</code>, <code>bodyContent</code>, <code>dueDateTime {dateTime, timeZone}</code>, <code>importance</code></td></tr><tr><td><strong>Detalle</strong></td><td><code>GET /me/todo/lists/{listId}/tasks/{taskId}</code></td><td><code>?$expand=assignments,linkedResources</code></td></tr><tr><td><strong>Actualizar</strong></td><td><code>PATCH /me/todo/lists/{listId}/tasks/{taskId}</code></td><td><code>status: 'completed'</code>, <code>completedDateTime</code></td></tr><tr><td><strong>Eliminar</strong></td><td><code>PATCH /me/todo/lists/{listId}/tasks/{taskId}</code></td><td><code>{"status": "deleted"}</code> (soft delete) </td></tr></tbody></table>

**Task Campos Esenciales**:

<pre class="language-json"><code class="lang-json"><strong>{
</strong>  "title": "Comprar leche",
  "bodyContent": "&#x3C;p>Lista supermercado&#x3C;/p>",
  "dueDateTime": {"dateTime": "2026-02-12T18:00:00Z", "timeZone": "Europe/Madrid"},
  "reminderDateTime": {...},
  "importance": "high",
  "status": "notStarted",
  "priority": 1,
  "recurrence": {...},
  "linkedResources": [{"webUrl": "https://...", "displayName": "Email"}],
  "categories": ["Urgente", "Casa"],
  "checklistItems": [{"title": "Leche entera", "isChecked": false}]
}
</code></pre>

**Gráfico: Estructura To Do**

```
me/todo/
├── lists/          # Listas (ej. "Tasks", "Compras")
│   └── {listId}/
│       └── tasks/  # Tasks de esa lista
│           └── {taskId} (CRUD)
```

#### Uso Rápido Python <a href="#uso-rpido-python-5-min" id="uso-rpido-python-5-min"></a>

{% code overflow="wrap" expandable="true" %}

```python
import requests

token = "tu_token"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 1. Crear lista
list_payload = {"displayName": "CursoGraph"}
list_resp = requests.post("https://graph.microsoft.com/v1.0/me/todo/lists", 
                         headers=headers, json=list_payload).json()
list_id = list_resp["id"]

# 2. Crear task
task_payload = {
    "title": "Leer inbox",
    "dueDateTime": {"dateTime": "2026-02-12T17:00:00Z", "timeZone": "UTC"}
}
task_resp = requests.post(f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks", 
                         headers=headers, json=task_payload).json()
print(f"Task ID: {task_resp['id']}")

# 3. Pendientes
pending = requests.get(f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks?$filter=status eq 'notStarted'", 
                      headers=headers).json()["value"]
```

{% endcode %}

#### Filtros Útiles \&expand <a href="#filtros-tiles-expand" id="filtros-tiles-expand"></a>

* `$filter=importance eq 'high' and dueDateTime le 2026-02-15T23:59:59Z`
* `$orderby=importance,dueDateTime`
* `$expand=linkedResources` (emails/calendario)
* **Todos Pendientes**: `GET /me/todo/lists/{id}/tasks?$filter=status ne 'completed'`

#### Graph Explorer:

1. `GET /me/todo/lists` → nota ID "Tasks".
2. `POST /me/todo/lists/{id}/tasks` con payload simple.
3. `GET /me/todo/lists/{id}/tasks?$filter=...` pendientes.

#### [Referencia](https://learn.microsoft.com/en-us/graph/api/resources/todo-overview?view=graph-rest-1.0)

#### Scenario 1: Correo → To-Do

{% code overflow="wrap" expandable="true" %}

```
Outlook Email
├─ Asunto: "Acción requerida: Revisar propuesta"
├─ De: cliente@empresa.com
├─ Cuerpo: "Necesito feedback para el martes"
└─ Adjuntos: propuesta.pdf

↓ Trigger: Asunto contiene "Acción requerida"

To Do Task (Lista: "Cliente A" o "Tasks")
├─ Título: "👤 Revisar propuesta - cliente@empresa.com"
├─ Descripción: "De: cliente@empresa.com\n\nNecesito feedback para el martes\n\nEnlace: https://outlook.office.com/mail/item/{msgId}"
├─ DueDateTime: "2026-02-17T18:00:00.0000000Z" (martes próximo)
├─ Reminder: 1h antes
├─ Importance: high
├─ Status: notStarted
└─ LinkedResources: Email URL + adjunto

```

{% endcode %}

#### Scenario 2: Evento → To-Do

{% code overflow="wrap" expandable="true" %}

```
Calendar Event
├─ Asunto: "Reunión: Planificación Q1"
├─ Hora: Lunes 14:00 (startDateTime)
├─ Asistentes: 5 personas (attendees)
└─ Descripción: "Definir OKRs"

↓ Trigger: Duración ~1h y contiene "organización"/"reunión"

To Do Task (Lista: "Estrategia")
├─ Título: "📅 Seguimiento: Planificación Q1"
├─ Descripción: "Reunión Lunes 14:00 (5 asistentes)\nOKRs: Definir OKRs\nEnlace: https://outlook.office.com/calendar/item/{eventId}"
├─ DueDateTime: Martes 14:00 (día después)
├─ Reminder: 9:00 martes
├─ Importance: high
├─ Status: notStarted
└─ LinkedResources: Calendar event URL

```

{% endcode %}

#### Opciones de Trigger

<table><thead><tr><th width="259">Trigger</th><th width="138">Tipo</th><th>Filtro</th></tr></thead><tbody><tr><td>Palabra clave en asunto</td><td>Correo</td><td>"Acción requerida", "URGENTE"</td></tr><tr><td>Remitente específico</td><td>Correo</td><td>clientes@empresa.com</td></tr><tr><td>Categoría/Etiqueta</td><td>Correo</td><td>"Cliente", "Proyecto"</td></tr><tr><td>Importancia</td><td>Correo</td><td>High importance</td></tr><tr><td>Duración evento</td><td>Evento</td><td>> 30 minutos</td></tr><tr><td>Organizador</td><td>Evento</td><td>usuarios específicos</td></tr><tr><td>Hora (business hours)</td><td>Evento</td><td>8 AM - 6 PM</td></tr></tbody></table>

#### 2. Convertir Correo a To-Do

#### Obtener Correos con Filtro

{% code title="A7\_1\_get\_emails\_to\_convert.py" overflow="wrap" expandable="true" %}

```python
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
```

{% endcode %}

#### Crear To-Do

{% code title="A7\_2\_create\_task\_from\_email.py" overflow="wrap" expandable="true" %}

```python
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  # pip install python-dateutil
from A0_1_get_token import get_delegated_token

SCOPES = ["Mail.ReadWrite"]
token = get_delegated_token(SCOPES)

def get_todo_list_id(access_token, list_name="EmailTasks"):
    """Obtiene o crea lista To Do."""
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    
    # GET listas
    response = requests.get("https://graph.microsoft.com/v1.0/me/todo/lists", headers=headers)
    if response.status_code == 200:
        lists = response.json().get("value", [])
        for lst in lists:
            if lst["displayName"] == list_name:
                return lst["id"]
    
    # Crea nueva
    create_payload = {"displayName": list_name, "is_shared": False}
    response = requests.post("https://graph.microsoft.com/v1.0/me/todo/lists", 
                            headers=headers, json=create_payload)
    if response.status_code == 201:
        print(f"✓ Lista creada: {list_name}")
        return response.json()["id"]
    return None

def create_task_from_email(access_token, email, list_name="EmailTasks"):
    """Convierte correo en tarea To Do (migrado de Planner)."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Extraer info email (igual)
    subject = email["subject"][:100]  # To Do title max ~250, pero seguro
    body_preview = email["bodyPreview"][:1000]  # bodyContent más flexible
    from_address = email["from"]["emailAddress"]["address"]
    msg_id = email["id"]
    msg_web_url = f"https://outlook.office.com/mail/item/{msg_id}"
    
    # Descripción mejorada
    description = f"""📧 CONVERTIDO DE EMAIL

👤 De: {from_address}
📋 Asunto: {email['subject']}
🔗 [Abrir Email]({msg_web_url})

📝 Preview:
{body_preview}

---
Creado: {datetime.now().strftime('%Y-%m-%d %H:%M')}"""

    # DueDate: 3 días por default
    due_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%dT18:00:00.0000000Z")
    
    # Payload To Do
    payload = {
        "title": f"📧 {subject}",
        "bodyContent": description,
        "bodyContentType": "html",  # Soporta Markdown-ish
        "dueDateTime": {
            "dateTime": due_date,
            "timeZone": "Europe/Madrid"
        },
        "reminderDateTime": {
            "dateTime": (datetime.now() + timedelta(days=3, hours=-2)).strftime("%Y-%m-%dT16:00:00.0000000Z"),
            "timeZone": "Europe/Madrid"
        },
        "importance": "high",
        "status": "notStarted",
        "linkedResources": [{
            "webUrl": msg_web_url,
            "applicationName": "Outlook",
            "displayName": f"Email: {subject}"
        }]
    }
    
    # GET/Crea lista
    list_id = get_todo_list_id(access_token, list_name)
    if not list_id:
        print("✗ Error obteniendo lista To Do")
        return None
    
    # POST task
    url = f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks"
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        task_id = response.json().get("id")
        print(f"✓ To Do Task creada en '{list_name}': {task_id}")
        print(f"  📱 Ver en: https://to-do.microsoft.com/tasks/{list_id}/{task_id}")
        return response.json()
    else:
        print(f"✗ Error To Do: {response.status_code}")
        print(response.text)
        return None

```

{% endcode %}

#### Lógica Completa con Validación

{% code title="A7\_3\_process\_emails\_to\_tasks.py" overflow="wrap" expandable="true" %}

```python
from A0_1_get_token import get_delegated_token
from A7_1_get_emails_to_convert import get_emails_to_convert
from A7_2_create_task_from_email import create_task_from_email
import requests

SCOPES = ["Mail.ReadWrite"]
token = get_delegated_token(SCOPES)

def process_emails_to_tasks(access_token, plan_id, bucket_id, assigned_user_id, keywords=None):
    """Procesa correos y crea tareas automáticamente."""
    
    # Obtener correos válidos
    emails = get_emails_to_convert(access_token, keywords=keywords)
    
    created_tasks = []
    
    for email in emails:
        try:
            # Validaciones
            if not email["subject"] or len(email["subject"]) < 3:
                print(f"⊘ Asunto muy corto: {email['subject']}")
                continue
            
            # Crear tarea
            task = create_task_from_email(
                access_token,
                email,
                plan_id,
                bucket_id,
                assigned_user_id
            )
            
            if task:
                created_tasks.append({
                    "email_subject": email["subject"],
                    "task_id": task.get("id"),
                    "status": "created"
                })
                
                # Marcar correo como leído (opcional)
                mark_email_as_read(access_token, email["id"])
        
        except Exception as e:
            print(f"✗ Error procesando correo: {e}")
            continue
    
    print(f"\n✓ Total de tareas creadas: {len(created_tasks)}")
    return created_tasks

def mark_email_as_read(access_token, message_id):
    """Marca un correo como leído."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {"isRead": True}
    
    requests.patch(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}",
        headers=headers,
        json=payload
    )
```

{% endcode %}

#### 3. Convertir Evento a To-Do

#### Obtener Eventos para Convertir

{% code overflow="wrap" expandable="true" %}

```python
def get_events_to_convert(access_token, hours_ahead=48):
    """Obtiene eventos que deben convertirse en tareas de seguimiento."""
    from datetime import datetime, timedelta
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    now = datetime.utcnow()
    future = now + timedelta(hours=hours_ahead)
    
    params = {
        "startDateTime": now.isoformat() + "Z",
        "endDateTime": future.isoformat() + "Z",
        "$select": "id,subject,start,end,organizer,attendees,bodyPreview,isOrganizer",
        "$filter": "isReminderOn eq true",  # Solo eventos importantes
        "$orderby": "start/dateTime"
    }
    
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me/calendarView",
        headers=headers,
        params=params
    )
    
    events = response.json().get("value", []) if response.status_code == 200 else []
    
    # Filtrar: solo eventos > 30 min y que soy organizador
    filtered = []
    for event in events:
        start = datetime.fromisoformat(event["start"]["dateTime"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(event["end"]["dateTime"].replace("Z", "+00:00"))
        duration_minutes = (end - start).total_seconds() / 60
        
        if duration_minutes >= 30 and event.get("isOrganizer", False):
            filtered.append(event)
    
    return filtered
```

{% endcode %}

#### Crear To-Do de Seguimiento

{% code overflow="wrap" expandable="true" %}

```python
import requests
from datetime import datetime, timedelta
from dateutil import parser  # pip install python-dateutil

def get_todo_list_id(access_token, list_name="EventFollowups"):
    """Obtiene o crea lista To Do para followups."""
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    
    # GET listas
    response = requests.get("https://graph.microsoft.com/v1.0/me/todo/lists", headers=headers)
    if response.status_code == 200:
        lists = response.json().get("value", [])
        for lst in lists:
            if lst["displayName"] == list_name:
                return lst["id"]
    
    # Crea
    create_payload = {"displayName": list_name, "is_shared": False}
    response = requests.post("https://graph.microsoft.com/v1.0/me/todo/lists", 
                            headers=headers, json=create_payload)
    if response.status_code == 201:
        print(f"✓ Lista creada: {list_name}")
        return response.json()["id"]
    return None

def create_task_from_event(access_token, event, list_name="EventFollowups"):
    """Crea task de seguimiento To Do desde evento (migrado Planner)."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Extraer info (igual + mejoras)
    subject = event["subject"][:200]  # To Do más flexible
    organizer = event["organizer"]["emailAddress"]["name"]
    attendees_count = len(event.get("attendees", []))
    body_preview = event.get("bodyPreview", "")[:1500]
    event_id = event["id"]
    event_web_url = f"https://outlook.office.com/calendar/item/{event_id}"
    
    # Título
    task_title = f"📅 Seguimiento: {subject}"
    
    # DueDate: día después (mejorado con TZ)
    event_end = parser.parse(event["end"]["dateTime"])
    due_dt = event_end + timedelta(days=1)
    due_date = due_dt.strftime("%Y-%m-%dT14:00:00.0000000Z")  # 14:00 martes
    
    # Descripción HTML/MD rica
    description = f"""📋 **SEGUIMIENTO DE EVENTO**

**Organizado por:** {organizer}  
**📊 Asistentes:** {attendees_count}  
**📅 Fecha reunión:** {event['start']['dateTime']} - {event['end']['dateTime']}  
**🔗** [Abrir Evento]({event_web_url})

**Resumen:**
{body_preview}

### ✅ **Acciones Pendientes:**
- [ ] Consolidar decisiones tomadas
- [ ] Asignar responsables
- [ ] Comunicar resultados al equipo
- [ ] Actualizar Planner/To Do

---
*Auto-creado: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}*"""

    # Payload To Do
    payload = {
        "title": task_title,
        "bodyContent": description,
        "bodyContentType": "html",
        "dueDateTime": {
            "dateTime": due_date,
            "timeZone": "Europe/Madrid"
        },
        "reminderDateTime": {
            "dateTime": (due_dt - timedelta(hours=4)).strftime("%Y-%m-%dT10:00:00.0000000Z"),
            "timeZone": "Europe/Madrid"
        },
        "importance": "high",
        "status": "notStarted",
        "categories": ["📋 Seguimiento", "🔄 Evento"],
        "linkedResources": [{
            "webUrl": event_web_url,
            "applicationName": "Outlook Calendar",
            "displayName": f"Reunión: {subject}"
        }]
    }
    
    # Lista
    list_id = get_todo_list_id(access_token, list_nam

```

{% endcode %}

#### Buenas Prácticas

#### ✅ Recomendaciones

* **Validar antes de convertir**: Verificar asunto, cuerpo y metadata
* **Usar transacciones**: Registro de auditoría para cada conversión
* **Manejo de duplicados**: Verificar si tarea ya existe
* **Preservar contexto**: Incluir email original/evento en descripción
* **Respetar preferencias**: Permitir configuración por usuario
* **Testing**: Probar con datos reales antes de automatizar

#### <mark style="color:$primary;">Ejercicio: Crear Tarea Simple desde Correo</mark>

<mark style="color:$primary;">Crea un To-Do por cada e-mail del jefe que incluya "por favor"</mark>

***

### Errores comunes (permisos, throttling) y mitigaciones

#### 1. Errores de Autenticación (401)&#x20;

#### ¿Qué es un 401?

El error **401 Unauthorized** significa que el servidor no reconoce tu token de acceso.

```
❌ 401 Unauthorized
┌─────────────────────────────────────┐
│ Token inválido, expirado o faltante │
└─────────────────────────────────────┘
```

#### Causas Comunes

<table><thead><tr><th width="215">Causa</th><th width="217">Síntoma</th><th>Solución</th></tr></thead><tbody><tr><td>Token expirado</td><td>Solicitud sin respuesta</td><td>Renovar token</td></tr><tr><td>Token inválido</td><td>Siempre 401</td><td>Verificar credenciales</td></tr><tr><td>Token incorrecto</td><td>401 intermitente</td><td>Usar MSAL con caché</td></tr><tr><td>Header incorrecto</td><td>Bearer token mal formado</td><td><code>Authorization: Bearer {token}</code></td></tr><tr><td>Sin token</td><td>Header vacío</td><td>Autenticar primero</td></tr></tbody></table>

#### 2. Errores de Permisos (403)&#x20;

#### ¿Qué es un 403?

El error **403 Forbidden** significa que el token es válido, pero no tienes permisos para esa operación.

```
❌ 403 Forbidden
┌──────────────────────────────────┐
│ Token válido pero sin permisos   │
└──────────────────────────────────┘
```

#### Causas Comunes

| Causa                      | Síntoma                    | Solución                    |
| -------------------------- | -------------------------- | --------------------------- |
| Permisos insuficientes     | 403 en endpoint específico | Agregar permiso en Azure AD |
| Tipo de permiso incorrecto | 403 aunque tienen permiso  | Usar delegado o aplicación  |
| Consentimiento no otorgado | 403 para usuario           | User da consentimiento      |
| Admin no aprobó            | 403 en multi-tenant        | Admin aprueba permisos      |
| Recurso sin acceso         | 403 a usuario específico   | Verificar acceso a recurso  |

#### Tabla de Permisos

```
Operación              │ Permiso Requerido      │ Tipo
───────────────────────┼────────────────────────┼──────────
Leer correos           │ Mail.Read              │ Delegado
Enviar correos         │ Mail.Send              │ Delegado
Leer calendario        │ Calendar.Read          │ Delegado
Crear eventos          │ Calendar.ReadWrite     │ Delegado
Leer todos los usuarios│ User.Read.All          │ Aplicación
Crear usuario          │ User.ReadWrite.All     │ Aplicación
Leer Planner           │ Planner.Read           │ Delegado
Crear tarea            │ Planner.ReadWrite      │ Delegado
```

#### 3. Throttling (429)&#x20;

#### ¿Qué es Throttling?

El error **429 Too Many Requests** significa que estás enviando demasiadas solicitudes demasiado rápido.

```
🚦 429 Too Many Requests
┌──────────────────────────────────────┐
│ Límite de velocidad alcanzado        │
│ Retry-After: 120 (espera 120 segundos)
└──────────────────────────────────────┘
```

#### Límites por Servicio

| Servicio   | Límite   | Ventana  | Costo    |
| ---------- | -------- | -------- | -------- |
| Mail       | 3000     | 10 min   | Alto     |
| Calendar   | 3000     | 10 min   | Alto     |
| Users      | 2000     | 10 min   | Medio    |
| Planner    | 1500     | 10 min   | Medio    |
| SharePoint | Dinámico | Variable | Muy Alto |

***

### Trazabilidad y auditoría mínima de operaciones

#### ¿Por Qué Auditar?

```
Motivos Legales
  └─ GDPR, HIPAA, SOX, ISO 27001
  └─ Demostrar cumplimiento

Motivos Operacionales
  └─ Debugging de problemas
  └─ Investigación de incidentes
  └─ Análisis de rendimiento

Motivos de Seguridad
  └─ Detectar accesos no autorizados
  └─ Identificar cambios maliciosos
  └─ Forensica digital
```

#### Información Mínima a Auditar

```
WHO     ¿Quién?        → Usuario/App ID
WHAT    ¿Qué?          → Operación realizada
WHEN    ¿Cuándo?       → Timestamp
WHERE   ¿Dónde?        → IP, Ubicación
WHY     ¿Por qué?      → Contexto
HOW     ¿Cómo?         → Método/Protocolo
RESULT  ¿Resultado?    → Éxito/Fallo
```

#### Arquitectura de Auditoría

```
Operación en Graph API
         ↓
Captura automática
         ↓
Enriquecimiento de datos
         ↓
Almacenamiento inmutable
         ↓
Análisis y alertas
         ↓
Reportes de compliance
```

#### Niveles de Auditoría

```
Nivel 1 - Mínimo (Obligatorio)
  • Usuario y timestamp
  • Operación (GET, POST, DELETE)
  • Endpoint accedido
  • Status code

Nivel 2 - Estándar (Recomendado)
  • Todo nivel 1
  • IP origen
  • Resultado (éxito/fallo)
  • Tamaño de datos

Nivel 3 - Completo (Cumplimiento)
  • Todo nivel 2
  • Body de request (sensibles masking)
  • Response summary
  • Detalles de error
  • Session info
```

#### 2. Implementación de Auditoría&#x20;

#### Decorator de Auditoría Automática

{% code title="A9\_1\_auditor.py" overflow="wrap" expandable="true" %}

```python
import logging
import json
from datetime import datetime
from functools import wraps
import uuid
import requests
from A0_1_get_token import get_delegated_token

SCOPES = ["Mail.ReadWrite"]
token = get_delegated_token(SCOPES)

# Configurar logger de auditoría
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

handler = logging.FileHandler("audit.log")
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
audit_logger.addHandler(handler)

def audit_operation(operation_type="API_CALL"):
    """Decorator para auditar operaciones automáticamente."""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generar ID único para operación
            operation_id = str(uuid.uuid4())
            
            # Registrar inicio
            start_time = datetime.utcnow()
            
            audit_entry = {
                "operation_id": operation_id,
                "operation_type": operation_type,
                "function": func.__name__,
                "timestamp": start_time.isoformat(),
                "status": "started"
            }
            
            try:
                # Ejecutar función
                result = func(*args, **kwargs)
                
                # Registrar éxito
                end_time = datetime.utcnow()
                duration_ms = (end_time - start_time).total_seconds() * 1000
                
                audit_entry.update({
                    "status": "success",
                    "duration_ms": duration_ms,
                    "timestamp_end": end_time.isoformat(),
                    "result_summary": str(result)[:100]  # Primeros 100 chars
                })
                
                audit_logger.info(json.dumps(audit_entry))
                return result
            
            except Exception as e:
                # Registrar error
                end_time = datetime.utcnow()
                duration_ms = (end_time - start_time).total_seconds() * 1000
                
                audit_entry.update({
                    "status": "failed",
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "duration_ms": duration_ms,
                    "timestamp_end": end_time.isoformat()
                })
                
                audit_logger.warning(json.dumps(audit_entry))
                raise
        
        return wrapper
    return decorator

# Uso
@audit_operation("GET_EMAILS")
def get_user_emails(access_token, top=10):
    """Obtiene correos del usuario."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/me/messages?$top={top}",
        headers=headers
    )
    return response.json()
```

{% endcode %}

#### 4. Buenas Prácticas de Auditoría&#x20;

#### ✅ Recomendaciones

{% code overflow="wrap" expandable="true" %}

```python
# 1. AUDITAR SIEMPRE (sin excepciones)
@audit_operation("CRITICAL_OPERATION")
def delete_user(user_id):
    # Auditar ANTES de hacer cambios
    pass

# 2. ENMASCARAR DATOS SENSIBLES
def sanitize_for_audit(data):
    """Enmascara datos sensibles."""
    
    sensitive_fields = ["password", "token", "secret"]
    
    for key in sensitive_fields:
        if key in data:
            data[key] = "***REDACTED***"
    
    return data

# 3. USAR TIMESTAMPS UTC
from datetime import datetime, timezone

timestamp = datetime.now(timezone.utc).isoformat()

# 4. INCLUIR CONTEXTO
audit_entry = {
    "who": user_id,
    "what": operation,
    "when": timestamp,
    "where": client_ip,
    "why": reason,
    "how": method,
    "result": status
}
```

{% endcode %}

***

### Ejemplos listos para reutilizar (snippets de correo/calendario) usando Graph SDK

#### 1. El Problema: Código Repetido&#x20;

```
❌ SIN SNIPPETS:
[Nuevo proyecto]
    ↓ Escribir código Graph desde cero
    ↓ Debuggear errores
    ↓ Agregar retry logic
    ↓ Test en producción
    ↓ 5+ horas por feature

✅ CON SNIPPETS:
[Nuevo proyecto]
    ↓ Copy-paste snippet
    ↓ Personalizar 5 minutos
    ↓ Ya tiene retry, error handling
    ↓ Deploy directo
    ↓ 15 minutos total

VENTAJAS:
├─ Código probado en producción
├─ Error handling incluido
├─ Documentación built-in
├─ Rápido copy-paste
└─ Zero debugging
```

#### Python Graph SDK Core

**`pip install msgraph-core`**

Hay que crear un **GraphClient** donde se alimenta el token

#### 2. Leer Emails

#### Snippet: Leer últimos N emails

{% code overflow="wrap" expandable="true" %}

```python
from msgraph.core import GraphClient
from typing import List, Dict

def get_recent_messages(client: GraphClient, limit: int = 10) -> List[Dict]:
    """
    Obtiene los últimos N emails.
    
    Args:
        client: Authenticated GraphClient
        limit: Cantidad de emails (default 10)
    
    Returns:
        List de emails con id, subject, from, date, preview
    
    Raises:
        Exception: Si hay error en API
    """
    
    try:
        # Query con paginación
        response = client.get(
            '/me/messages',
            params={
                '$top': limit,
                '$orderby': 'receivedDateTime desc',
                '$select': 'id,subject,from,receivedDateTime,bodyPreview,isRead'
            }
        )
        
        messages = []
        for msg in response['value']:
            messages.append({
                'id': msg['id'],
                'subject': msg['subject'],
                'from': msg['from']['emailAddress']['address'],
                'from_name': msg['from']['emailAddress']['name'],
                'date': msg['receivedDateTime'],
                'preview': msg['bodyPreview'],
                'is_read': msg['isRead']
            })
        
        return messages
    
    except Exception as e:
        print(f"Error getting messages: {e}")
        raise

# Crea GraphClient con token
def create_graph_client_from_token(token: str) -> GraphClient:
    """GraphClient usando token existente."""
    client = GraphClient(
        credential=lambda: ({'access_token': token}),  # Lambda retorna dict token
        # Opcional: user email para logging
        account="tu-email@domain.com"  # De /me o claims
    )
    return client

# USO (exacto tu código)
client = create_graph_client_from_token(ACCESS_TOKEN)

messages = get_recent_messages(client, limit=20)
for msg in messages:
    print(f"[{msg['date']}] {msg['from_name']}: {msg['subject']}")
```

{% endcode %}

#### 3. Buscar Emails por Asunto&#x20;

#### Snippet: Búsqueda avanzada

{% code overflow="wrap" expandable="true" %}

```python
def search_messages_by_subject(client: GraphClient, subject: str) -> List[Dict]:
    """Busca emails por asunto."""
    
    try:
        response = client.get(
            '/me/messages',
            params={
                '$filter': f"contains(subject, '{subject}')",
                '$select': 'id,subject,from,receivedDateTime,hasAttachments',
                '$top': 50
            }
        )
        
        return response['value']
    
    except Exception as e:
        print(f"Search error: {e}")
        return []

# USO
results = search_messages_by_subject(client, "Invoice")
print(f"Found {len(results)} emails with 'Invoice'")
```

{% endcode %}

#### 4. Leer Email Completo con Attachments&#x20;

#### Snippet: Email + archivos

{% code overflow="wrap" expandable="true" %}

```python
def get_message_with_attachments(client: GraphClient, message_id: str) -> Dict:
    """Obtiene email completo con attachments."""
    
    try:
        # Obtener mensaje
        message = client.get(f'/me/messages/{message_id}')
        
        # Obtener attachments
        attachments = client.get(f'/me/messages/{message_id}/attachments')
        
        result = {
            'id': message['id'],
            'subject': message['subject'],
            'from': message['from']['emailAddress']['name'],
            'date': message['receivedDateTime'],
            'body': message['bodyPreview'],
            'attachments': []
        }
        
        # Procesar attachments
        for att in attachments['value']:
            result['attachments'].append({
                'id': att['id'],
                'name': att['name'],
                'type': att['@odata.type'],
                'size': att.get('size', 0)
            })
        
        return result
    
    except Exception as e:
        print(f"Error: {e}")
        raise

# USO
msg = get_message_with_attachments(client, "message_id")
print(f"Email: {msg['subject']}")
print(f"Attachments: {len(msg['attachments'])}")
for att in msg['attachments']:
    print(f"  - {att['name']} ({att['size']} bytes)")
```

{% endcode %}

#### 5. Enviar Email Simple&#x20;

#### Snippet: Enviar mensaje

{% code overflow="wrap" expandable="true" %}

```python
def send_email(client: GraphClient, to: str, subject: str, body: str) -> bool:
    """Envía un email simple."""
    
    try:
        message = {
            'subject': subject,
            'body': {
                'contentType': 'HTML',
                'content': body
            },
            'toRecipients': [
                {
                    'emailAddress': {
                        'address': to
                    }
                }
            ]
        }
        
        client.post('/me/sendMail', {'message': message})
        return True
    
    except Exception as e:
        print(f"Send error: {e}")
        return False

# USO
send_email(
    client,
    to='user@example.com',
    subject='Hello',
    body='<p>This is an HTML email</p>'
)
```

{% endcode %}

#### 6. Enviar Email con CC/BCC&#x20;

#### Snippet: Email avanzado

{% code overflow="wrap" expandable="true" %}

```python
def send_email_advanced(
    client: GraphClient,
    to: List[str],
    cc: List[str] = None,
    bcc: List[str] = None,
    subject: str = '',
    body: str = ''
) -> bool:
    """Envía email con CC/BCC."""
    
    try:
        # Construir recipients
        to_recipients = [{'emailAddress': {'address': addr}} for addr in to]
        cc_recipients = [{'emailAddress': {'address': addr}} for addr in (cc or [])]
        bcc_recipients = [{'emailAddress': {'address': addr}} for addr in (bcc or [])]
        
        message = {
            'subject': subject,
            'body': {'contentType': 'HTML', 'content': body},
            'toRecipients': to_recipients,
            'ccRecipients': cc_recipients,
            'bccRecipients': bcc_recipients
        }
        
        client.post('/me/sendMail', {'message': message})
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False

# USO
send_email_advanced(
    client,
    to=['user1@example.com', 'user2@example.com'],
    cc=['manager@example.com'],
    subject='Meeting Summary',
    body='<p>Notes from our meeting...</p>'
)
```

{% endcode %}

#### 7. Crear Evento Calendario&#x20;

#### Snippet: Crear evento

{% code overflow="wrap" expandable="true" %}

```python
from datetime import datetime, timedelta

def create_event(
    client: GraphClient,
    title: str,
    start_time: datetime,
    duration_minutes: int = 60,
    attendees: List[str] = None,
    location: str = None
) -> Dict:
    """Crea un evento en el calendario."""
    
    try:
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        # Construir attendees
        attendee_list = []
        if attendees:
            for email in attendees:
                attendee_list.append({
                    'emailAddress': {'address': email},
                    'type': 'required'
                })
        
        event = {
            'subject': title,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC'
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC'
            },
            'attendees': attendee_list,
            'location': {'displayName': location} if location else None,
            'isReminderOn': True,
            'reminderMinutesBeforeStart': 15
        }
        
        response = client.post('/me/events', event)
        return response
    
    except Exception as e:
        print(f"Event creation error: {e}")
        raise

# USO
event = create_event(
    client,
    title='Team Meeting',
    start_time=datetime.now() + timedelta(days=1, hours=2),
    duration_minutes=60,
    attendees=['team@example.com'],
    location='Conference Room A'
)
print(f"Event created: {event['id']}")
```

{% endcode %}

#### 8. Obtener Eventos Este Mes&#x20;

#### Snippet: Buscar eventos

{% code overflow="wrap" expandable="true" %}

```python
def get_events_this_month(client: GraphClient) -> List[Dict]:
    """Obtiene eventos del mes actual."""
    
    from datetime import datetime
    
    try:
        today = datetime.now()
        start = today.replace(day=1)
        end = (start + timedelta(days=32)).replace(day=1)
        
        response = client.get(
            '/me/calendarview',
            params={
                'startDateTime': start.isoformat(),
                'endDateTime': end.isoformat(),
                '$select': 'subject,start,end,attendees',
                '$orderby': 'start/dateTime'
            }
        )
        
        return response['value']
    
    except Exception as e:
        print(f"Error: {e}")
        return []

# USO
events = get_events_this_month(client)
for event in events:
    print(f"{event['subject']} - {event['start']['dateTime']}")
```

{% endcode %}

#### 9. Actualizar Evento&#x20;

#### Snippet: Modificar evento

{% code overflow="wrap" expandable="true" %}

```python
def update_event(
    client: GraphClient,
    event_id: str,
    subject: str = None,
    start_time: datetime = None,
    end_time: datetime = None
) -> bool:
    """Actualiza un evento existente."""
    
    try:
        update_data = {}
        
        if subject:
            update_data['subject'] = subject
        
        if start_time:
            update_data['start'] = {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC'
            }
        
        if end_time:
            update_data['end'] = {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC'
            }
        
        client.patch(f'/me/events/{event_id}', update_data)
        return True
    
    except Exception as e:
        print(f"Update error: {e}")
        return False

# USO
update_event(
    client,
    event_id='event_id',
    subject='Updated Meeting Title',
    start_time=datetime.now() + timedelta(hours=1)
)
```

{% endcode %}

#### 10. Marcar Emails como Leído&#x20;

#### Snippet: Actualizar estado

{% code overflow="wrap" expandable="true" %}

```python
def mark_as_read(client: GraphClient, message_id: str) -> bool:
    """Marca un email como leído."""
    
    try:
        client.patch(
            f'/me/messages/{message_id}',
            {'isRead': True}
        )
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False

def mark_as_unread(client: GraphClient, message_id: str) -> bool:
    """Marca un email como no leído."""
    
    try:
        client.patch(
            f'/me/messages/{message_id}',
            {'isRead': False}
        )
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False

# USO
mark_as_read(client, 'message_id')
```

{% endcode %}

#### 11. Mover Email a Carpeta&#x20;

#### Snippet: Organizar emails

{% code overflow="wrap" expandable="true" %}

```python
def move_message_to_folder(
    client: GraphClient,
    message_id: str,
    folder_id: str
) -> bool:
    """Mueve email a carpeta."""
    
    try:
        client.post(
            f'/me/messages/{message_id}/move',
            {'destinationId': folder_id}
        )
        return True
    
    except Exception as e:
        print(f"Move error: {e}")
        return False

# USO
# Primero obtener folder IDs
folders = client.get('/me/mailFolders')
archive_folder_id = folders['value'][0]['id']

move_message_to_folder(client, 'message_id', archive_folder_id)
```

{% endcode %}

#### 12. Eliminar Email&#x20;

#### Snippet: Borrar mensaje

{% code overflow="wrap" expandable="true" %}

```python
def delete_message(client: GraphClient, message_id: str) -> bool:
    """Elimina un email."""
    
    try:
        client.delete(f'/me/messages/{message_id}')
        return True
    
    except Exception as e:
        print(f"Delete error: {e}")
        return False

# USO
delete_message(client, 'message_id')
```

{% endcode %}

#### 13. Clase Integrada: MailManager&#x20;

{% code overflow="wrap" expandable="true" %}

```python
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class MailManager:
    """Gestor de correos production-ready."""
    
    def __init__(self, client: GraphClient):
        self.client = client
    
    def get_unread_count(self) -> int:
        """Obtiene cantidad de emails no leídos."""
        try:
            response = self.client.get(
                '/me/messages',
                params={'$filter': "isRead eq false", '$count': 'true'}
            )
            return response['@odata.count']
        except Exception as e:
            print(f"Error: {e}")
            return 0
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict]:
        """Obtiene últimos N emails."""
        try:
            response = self.client.get(
                '/me/messages',
                params={
                    '$top': limit,
                    '$orderby': 'receivedDateTime desc',
                    '$select': 'id,subject,from,receivedDateTime,isRead'
                }
            )
            return response['value']
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def search(self, query: str, limit: int = 50) -> List[Dict]:
        """Busca emails."""
        try:
            response = self.client.get(
                '/me/messages',
                params={
                    '$filter': f"contains(subject, '{query}') or contains(bodyPreview, '{query}')",
                    '$top': limit
                }
            )
            return response['value']
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def send(self, to: str, subject: str, body: str) -> bool:
        """Envía email."""
        try:
            message = {
                'subject': subject,
                'body': {'contentType': 'HTML', 'content': body},
                'toRecipients': [{'emailAddress': {'address': to}}]
            }
            self.client.post('/me/sendMail', {'message': message})
            return True
        except Exception as e:
            print(f"Send error: {e}")
            return False
    
    def mark_as_read(self, message_id: str) -> bool:
        """Marca como leído."""
        try:
            self.client.patch(f'/me/messages/{message_id}', {'isRead': True})
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

# USO
mail = MailManager(client)
unread = mail.get_unread_count()
recent = mail.get_recent_messages(limit=5)
search_results = mail.search("Invoice")

mail.send('user@example.com', 'Hello', '<p>Hi there!</p>')
mail.mark_as_read('message_id')
```

{% endcode %}

#### 14. Clase Integrada: CalendarManager&#x20;

{% code overflow="wrap" expandable="true" %}

```python
class CalendarManager:
    """Gestor de calendario production-ready."""
    
    def __init__(self, client: GraphClient):
        self.client = client
    
    def get_today_events(self) -> List[Dict]:
        """Eventos de hoy."""
        try:
            today = datetime.now()
            tomorrow = today + timedelta(days=1)
            
            response = self.client.get(
                '/me/calendarview',
                params={
                    'startDateTime': today.isoformat(),
                    'endDateTime': tomorrow.isoformat(),
                    '$orderby': 'start/dateTime'
                }
            )
            return response['value']
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def get_upcoming_events(self, days: int = 7) -> List[Dict]:
        """Eventos próximos N días."""
        try:
            today = datetime.now()
            future = today + timedelta(days=days)
            
            response = self.client.get(
                '/me/calendarview',
                params={
                    'startDateTime': today.isoformat(),
                    'endDateTime': future.isoformat(),
                    '$orderby': 'start/dateTime'
                }
            )
            return response['value']
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def create_event(self, title: str, start: datetime, duration: int = 60) -> Optional[str]:
        """Crea evento."""
        try:
            end = start + timedelta(minutes=duration)
            
            event = {
                'subject': title,
                'start': {'dateTime': start.isoformat(), 'timeZone': 'UTC'},
                'end': {'dateTime': end.isoformat(), 'timeZone': 'UTC'},
                'isReminderOn': True,
                'reminderMinutesBeforeStart': 15
            }
            
            response = self.client.post('/me/events', event)
            return response['id']
        except Exception as e:
            print(f"Create error: {e}")
            return None
    
    def delete_event(self, event_id: str) -> bool:
        """Elimina evento."""
        try:
            self.client.delete(f'/me/events/{event_id}')
            return True
        except Exception as e:
            print(f"Delete error: {e}")
            return False

# USO
calendar = CalendarManager(client)
today_events = calendar.get_today_events()
upcoming = calendar.get_upcoming_events(days=7)

event_id = calendar.create_event('Team Meeting', datetime.now() + timedelta(hours=1))
calendar.delete_event(event_id)
```

{% endcode %}

### &#xD;

***

## Cuestionario Sesión 5

Haz click [aquí](https://docs.google.com/forms/d/e/1FAIpQLSdZSuCPTMzobM1-TESlfW9lVUrpo7HlTnIN2ctK-qMFGBp7eQ/viewform?usp=sharing\&ouid=116231833500663506735) cuando lo indique el formador

## Feedback Sesión 5

Haz click [aquí](https://imagina-formacion.typeform.com/to/aE2zMr9b) cuando lo indique el formador
