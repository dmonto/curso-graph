import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url, timeout=10) as resp:
        resp.raise_for_status()
        return await resp.json()

async def main():
    async with aiohttp.ClientSession() as session:
        data = await fetch(session, "https://httpbin.org/json")
        print("Título:", data.get("slideshow", {}).get("title"))

if __name__ == "__main__":
    asyncio.run(main())