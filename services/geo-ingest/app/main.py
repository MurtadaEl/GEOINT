from fastapi import FastAPI
from pydantic import BaseModel

import asyncpg, os

app = FastAPI()

async def get_db():
    return await asyncpg.connect(
        host=os.getenv("DB_HOST", "postgis"),
        port=int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME", "geoint-db"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password")
    )

class GeoData(BaseModel):
    name: str
    coordinates: list[float]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tracks")
async def ingest_tracks(geo_data: GeoData):
    conn = await get_db()
    await conn.execute(
        "INSERT INTO assets (name, location) VALUES ($1, ST_MakePoint($2, $3))",
        geo_data.name, geo_data.coordinates[0], geo_data.coordinates[1]
    )
    await conn.close()
    return {"message": "Track data ingested successfully"}

