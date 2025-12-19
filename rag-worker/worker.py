import os
import httpx
from fastapi import FastAPI
from chromadb import Client

OLLAMA = os.getenv("OLLAMA_URL", "http://ollama:11434")

app = FastAPI()
db = Client()
collection = db.get_or_create_collection("nimbos")

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.post("/embed")
async def embed(text: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OLLAMA}/api/embeddings",
            json={"model": "phi3", "prompt": text}
        )
    emb = response.json()["embedding"]
    collection.add(documents=[text], embeddings=[emb])
    return {"status": "ok"}

@app.post("/query")
async def query(q: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OLLAMA}/api/embeddings",
            json={"model": "phi3", "prompt": q}
        )
    q_emb = response.json()["embedding"]
    result = collection.query(query_embeddings=[q_emb], n_results=3)
    return result
