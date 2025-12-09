from fastapi import FastAPI

app = FastAPI(title="NimbOS Brain API")

@app.get("/health")
def health():
    return {"status": "ok", "message": "NimbOS API running"}
