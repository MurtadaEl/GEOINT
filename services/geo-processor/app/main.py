from fastapi import FastAPI
from pydantic import BaseModel

import asyncpg, os

app = FastAPI()

class GeoData(BaseModel):
    name: str
    coordinates: list[float]

class NearbyQuery(BaseModel):
    lon: float
    lat: float
    radius_meters: float

async def get_db():
    return await asyncpg.connect(
        host=os.getenv("DB_HOST", "postgis"),
        port=int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME", "geoint-db"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password")
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/process")
async def process_geo_data(geo_data: GeoData):
    conn = await get_db()
    await conn.execute(
        "INSERT INTO assets (name, location) VALUES ($1, ST_MakePoint($2, $3))",
        geo_data.name, geo_data.coordinates[0], geo_data.coordinates[1]
    )
    await conn.close()

    return {"message": "stored", "data": geo_data}

@app.post("/nearby")
async def nearby_assets(query: NearbyQuery):
    conn = await get_db()
    rows = await conn.fetch(
        """
        SELECT id, name, ST_AsText(location) AS location
        FROM assets
        WHERE ST_DWithin(
            location,
            ST_MakePoint($1,$2)::geography,
            $3
        )
        """,
        query.lon, query.lat, query.radius_meters
    )
    await conn.close()
    return {"assets": [dict(row) for row in rows]}