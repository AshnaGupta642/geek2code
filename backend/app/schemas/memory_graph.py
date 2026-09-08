from pydantic import BaseModel, Field


class MemoryGraphRequest(BaseModel):
    memory_id: int = Field(gt=0)
    patient_id: int = Field(gt=0)

    people: list[str] = Field(default_factory=list)
    places: list[str] = Field(default_factory=list)
    events: list[str] = Field(default_factory=list)
    photo_ids: list[str] = Field(default_factory=list)


class MemoryGraphNode(BaseModel):
    id: str
    type: str
    label: str


class MemoryGraphRelationship(BaseModel):
    source_id: str
    target_id: str
    relationship_type: str


class MemoryGraphResponse(BaseModel):
    memory_id: int
    nodes: list[MemoryGraphNode] = Field(default_factory=list)
    relationships: list[MemoryGraphRelationship] = Field(default_factory=list)