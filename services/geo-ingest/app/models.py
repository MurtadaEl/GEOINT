from pydantic import BaseModel

class GeoData(BaseModel):
    name: str
    coordinates: list[float]
