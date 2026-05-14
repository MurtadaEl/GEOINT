from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tracks")
def ingest_tracks():
    # Placeholder for track ingestion logic
    return {"message": "Track data ingested successfully"}

