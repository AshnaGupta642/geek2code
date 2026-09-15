from pydantic import BaseModel, Field


class SafeZoneCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    radius_meters: float = Field(gt=0)


class SafeZoneUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    radius_meters: float | None = Field(default=None, gt=0)
    is_active: bool | None = None


class SafeZoneResponse(BaseModel):
    id: int
    patient_id: int
    name: str
    latitude: float
    longitude: float
    radius_meters: float
    is_active: bool

    class Config:
        from_attributes = True