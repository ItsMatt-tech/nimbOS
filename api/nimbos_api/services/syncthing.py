import httpx
from fastapi import HTTPException

SYNCTHING_API = "http://nimbos_syncthing:8384/rest"

# Get Syncthing API key from config later
API_KEY = "default-key (replace)"


async def get_status():
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{SYNCTHING_API}/system/status",
                headers={"X-API-Key": API_KEY}
            )
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
