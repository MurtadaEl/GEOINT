import asyncpg, os

async def get_db():
    return await asyncpg.connect(
        host=os.getenv("DB_HOST", "postgis"),
        port=int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME", "geoint-db"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password"),
    )

async def init_db():
    conn = await get_db()
    await conn.execute("""
        CREATE EXTENSION IF NOT EXISTS postgis;
        CREATE TABLE IF NOT EXISTS assets (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            location GEOMETRY(Point, 4326)
        );
    """)
    await conn.close()
