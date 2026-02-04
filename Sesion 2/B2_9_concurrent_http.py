import aiohttp
import asyncio

async def fetch_user(session, user_id, token):
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    async with session.get(url, headers=headers, timeout=10) as resp:
        if resp.status != 200:
            print("Error usuario", user_id, "status:", resp.status)
            return None
        return await resp.json()

async def obtener_muchos_usuarios(user_ids, token, max_concurrent=10):
    connector = aiohttp.TCPConnector(limit=max_concurrent)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_user(session, uid, token) for uid in user_ids]
        return await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Obtener token app_only
    # Incluir user_ids
    # users = asyncio.run(obtener_muchos_usuarios(["id1","id2","id3"], token))
    # Mostrar Datos
    pass