from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import get_db, init_db
from .models import GeoData

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tracks")
async def ingest_tracks(geo_data: GeoData):
    conn = await get_db()
    await conn.execute(
        "INSERT INTO assets (name, location) VALUES ($1, ST_SetSRID(ST_MakePoint($2, $3), 4326))",
        geo_data.name, geo_data.coordinates[0], geo_data.coordinates[1],
    )
    await conn.close()
    return {"message": "Track data ingested successfully"}
