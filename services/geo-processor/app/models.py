from pydantic import BaseModel

class GeoData(BaseModel):
    name: str
    coordinates: list[float]

class NearbyQuery(BaseModel):
    lon: float
    lat: float
    radius_meters: float