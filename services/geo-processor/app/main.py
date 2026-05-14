from fastapi import FastAPI
from pydantic import BaseModel

import asyncpg, os

app = FastAPI()

class GeoData(BaseModel):
    name: str
    coordinates: list[float]

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
        "INSERT INTO assets (name, coordinates) VALUES ($1, $2)",
        geo_data.name, str(geo_data.coordinates)
    )
    await conn.close()

    return {"message": "stored", "data": geo_data}
