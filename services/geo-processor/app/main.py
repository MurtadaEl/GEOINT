from fastapi import FastAPI
from .database import get_db
from .models import GeoData, NearbyQuery

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/process")
async def process_geo_data(geo_data: GeoData):
    conn = await get_db()
    await conn.execute(
        "INSERT INTO assets (name, location) VALUES ($1, ST_SetSRID(ST_MakePoint($2, $3), 4326))",
        geo_data.name, geo_data.coordinates[0], geo_data.coordinates[1],
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
            location::geography,
            ST_MakePoint($1, $2)::geography,
            $3
        )
        """,
        query.lon, query.lat, query.radius_meters,
    )
    await conn.close()
    return {"assets": [dict(row) for row in rows]}