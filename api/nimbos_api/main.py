from fastapi import FastAPI

app = FastAPI(title="NimbOS Brain API")

@app.get("/health")
def health():
    return {"status": "ok", "message": "NimbOS API running"}

from fastapi import APIRouter
from .services.syncthing import get_status

router = APIRouter()

@router.get("/syncthing/status")
async def syncthing_status():
    return await get_status()

app.include_router(router)
