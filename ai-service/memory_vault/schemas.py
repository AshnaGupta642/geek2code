"""
Schemas for the Memory Vault.

Defines the standard structure of:
- People
- Memory entities
- Structured memories
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


# ---------------------------------------------------------
# Person
# ---------------------------------------------------------

@dataclass
class Person:
    """A person mentioned in a patient's memory."""

    name: str
    relationship: str = ""

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        self.relationship = self.relationship.strip()
        if not self.name:
            raise ValueError("Person.name cannot be empty.")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Person":
        """Build a Person from a raw dict, e.g. from memory_extractor.py output."""
        return cls(
            name=str(data.get("name", "")),
            relationship=str(data.get("relationship", "")),
        )

    def to_dict(self) -> Dict[str, str]:
        return {"name": self.name, "relationship": self.relationship}


# ---------------------------------------------------------
# Entity
# ---------------------------------------------------------

@dataclass
class MemoryEntity:
    """
    An entity that can later become a node in the
    Memory Graph.
    """

    id: str
    type: str
    name: str
    relationship: str = ""

    def __post_init__(self) -> None:
        self.id = self.id.strip()
        self.type = self.type.strip().upper()
        self.name = self.name.strip()
        self.relationship = self.relationship.strip()

        if not self.id or not self.type or not self.name:
            raise ValueError("MemoryEntity requires non-empty id, type, and name.")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryEntity":
        """Build a MemoryEntity from a raw dict, e.g. from entity_extractor.py output."""
        return cls(
            id=str(data.get("id", "")),
            type=str(data.get("type", "")),
            name=str(data.get("name", "")),
            relationship=str(data.get("relationship", "")),
        )

    def to_dict(self) -> Dict[str, str]:
        result = {"id": self.id, "type": self.type, "name": self.name}
        if self.relationship:
            result["relationship"] = self.relationship
        return result


# ---------------------------------------------------------
# Structured Memory
# ---------------------------------------------------------

@dataclass
class StructuredMemory:
    """
    Complete structured representation of a patient's memory.
    """

    people: List[Person] = field(default_factory=list)
    places: List[str] = field(default_factory=list)
    events: List[str] = field(default_factory=list)
    dates: List[str] = field(default_factory=list)
    objects: List[str] = field(default_factory=list)
    emotions: List[str] = field(default_factory=list)
    summary: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StructuredMemory":
        """
        Build a StructuredMemory from the raw dict returned by
        memory_extractor.py (or memory_normalizer.py's normalize_memory()).
        Malformed person entries are skipped rather than raising, so one
        bad entry doesn't fail the whole memory.
        """
        people = []
        for person_data in data.get("people", []):
            if isinstance(person_data, dict) and str(person_data.get("name", "")).strip():
                people.append(Person.from_dict(person_data))

        return cls(
            people=people,
            places=[str(p) for p in data.get("places", []) if str(p).strip()],
            events=[str(e) for e in data.get("events", []) if str(e).strip()],
            dates=[str(d) for d in data.get("dates", []) if str(d).strip()],
            objects=[str(o) for o in data.get("objects", []) if str(o).strip()],
            emotions=[str(em) for em in data.get("emotions", []) if str(em).strip()],
            summary=str(data.get("summary", "")).strip(),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the structured memory to a dictionary."""
        return {
            "people": [person.to_dict() for person in self.people],
            "places": self.places,
            "events": self.events,
            "dates": self.dates,
            "objects": self.objects,
            "emotions": self.emotions,
            "summary": self.summary,
        }


# ---------------------------------------------------------
# Entity Collection
# ---------------------------------------------------------

@dataclass
class EntityCollection:
    """Collection of graph-ready memory entities."""

    entities: List[MemoryEntity] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EntityCollection":
        """
        Build an EntityCollection from the raw dict returned by
        entity_extractor.py. Malformed entities are skipped rather
        than raising, so one bad entity doesn't fail the whole collection.
        """
        entities = []
        for entity_data in data.get("entities", []):
            if not isinstance(entity_data, dict):
                continue
            try:
                entities.append(MemoryEntity.from_dict(entity_data))
            except ValueError:
                continue

        return cls(entities=entities)

    def to_dict(self) -> Dict[str, List[Dict[str, str]]]:
        """Convert entities to a dictionary."""
        return {"entities": [entity.to_dict() for entity in self.entities]}


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":
    memory = StructuredMemory(
        people=[Person(name="Ramesh", relationship="brother")],
        places=["Shillong", "Ward's Lake"],
        events=["Going to Ward's Lake every Sunday"],
        dates=[],
        objects=["blue school bag"],
        emotions=["happy"],
        summary="The patient remembers living in Shillong with their brother Ramesh.",
    )

    print("Structured Memory:")
    print(memory.to_dict())

    # Round-trip test: dict -> StructuredMemory -> dict
    rebuilt = StructuredMemory.from_dict(memory.to_dict())
    print("\nRound-tripped Structured Memory:")
    print(rebuilt.to_dict())

    entity_collection = EntityCollection(
        entities=[
            MemoryEntity(id="person_ramesh", type="PERSON", name="Ramesh", relationship="brother"),
            MemoryEntity(id="place_shillong", type="PLACE", name="Shillong"),
        ]
    )

    print("\nEntity Collection:")
    print(entity_collection.to_dict())

    # Round-trip test
    rebuilt_entities = EntityCollection.from_dict(entity_collection.to_dict())
    print("\nRound-tripped Entity Collection:")
    print(rebuilt_entities.to_dict())