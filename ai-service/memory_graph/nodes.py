"""
Memory Graph Nodes

Defines the different types of nodes used in the patient's memory graph.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

# ---------------------------------------------------------
# Supported node types
#
# Kept in sync with the types entity_extractor.py actually produces
# (PERSON, PLACE, EVENT, DATE, OBJECT, EMOTION) plus PATIENT, which
# graph_builder.py adds as the anchor node for relationship edges.
# PHOTO is reserved for a future feature and not yet produced upstream.
# ---------------------------------------------------------
PERSON = "PERSON"
PLACE = "PLACE"
EVENT = "EVENT"
DATE = "DATE"
OBJECT = "OBJECT"
EMOTION = "EMOTION"
PATIENT = "PATIENT"
PHOTO = "PHOTO"

ALL_NODE_TYPES = {PERSON, PLACE, EVENT, DATE, OBJECT, EMOTION, PATIENT, PHOTO}


@dataclass
class MemoryNode:
    """
    Represents a single node in the memory graph.
    """

    id: str
    type: str
    label: str
    relationship: Optional[str] = None

    def __post_init__(self) -> None:
        # Normalize the same way entity_extractor.py / schemas.py do,
        # so a stray lowercase type ("person") doesn't silently fail
        # validate_node() just because of casing.
        self.id = self.id.strip()
        self.type = self.type.strip().upper()
        self.label = self.label.strip()
        if self.relationship is not None:
            self.relationship = self.relationship.strip() or None

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary format."""
        node: Dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "label": self.label,
        }
        if self.relationship:
            node["relationship"] = self.relationship
        return node

    @classmethod
    def from_entity(cls, entity: Dict[str, Any]) -> "MemoryNode":
        """
        Build a MemoryNode from an entity dict as produced by
        entity_extractor.py (keys: id, type, name, relationship).
        Note the field rename: entity "name" -> node "label".
        """
        return cls(
            id=str(entity.get("id", "")),
            type=str(entity.get("type", "")),
            label=str(entity.get("name", "")),
            relationship=entity.get("relationship") or None,
        )


# ---------------------------------------------------------
# Factory functions
# ---------------------------------------------------------

def create_person_node(person_id: str, name: str, relationship: str = "") -> MemoryNode:
    """Create a PERSON node."""
    return MemoryNode(id=person_id, type=PERSON, label=name, relationship=relationship or None)


def create_place_node(place_id: str, name: str) -> MemoryNode:
    """Create a PLACE node."""
    return MemoryNode(id=place_id, type=PLACE, label=name)


def create_event_node(event_id: str, name: str) -> MemoryNode:
    """Create an EVENT node."""
    return MemoryNode(id=event_id, type=EVENT, label=name)


def create_date_node(date_id: str, label: str) -> MemoryNode:
    """Create a DATE node."""
    return MemoryNode(id=date_id, type=DATE, label=label)


def create_object_node(object_id: str, name: str) -> MemoryNode:
    """Create an OBJECT node."""
    return MemoryNode(id=object_id, type=OBJECT, label=name)


def create_emotion_node(emotion_id: str, name: str) -> MemoryNode:
    """Create an EMOTION node."""
    return MemoryNode(id=emotion_id, type=EMOTION, label=name)


def create_patient_node(patient_id: str = "patient", name: str = "Patient") -> MemoryNode:
    """Create the anchor PATIENT node that other nodes relate to."""
    return MemoryNode(id=patient_id, type=PATIENT, label=name)


def create_photo_node(photo_id: str, label: str = "Photo") -> MemoryNode:
    """Create a PHOTO node."""
    return MemoryNode(id=photo_id, type=PHOTO, label=label)


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

def validate_node(node: MemoryNode) -> bool:
    """
    Validate a memory graph node.

    Returns True if valid, otherwise False.
    """
    if not node.id:
        return False
    if not node.label:
        return False
    if node.type not in ALL_NODE_TYPES:
        return False
    return True


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    person = create_person_node("person_ramesh", "Ramesh", "brother")
    place = create_place_node("place_shillong", "Shillong")
    event = create_event_node("event_wedding", "Family Wedding")
    obj = create_object_node("object_school_bag", "Blue school bag")
    emotion = create_emotion_node("emotion_happy", "Happy")
    date = create_date_node("date_1998", "1998")
    patient = create_patient_node()

    print("Person:")
    print(person.to_dict())
    print("\nPlace:")
    print(place.to_dict())
    print("\nEvent:")
    print(event.to_dict())
    print("\nObject:")
    print(obj.to_dict())
    print("\nEmotion:")
    print(emotion.to_dict())
    print("\nDate:")
    print(date.to_dict())
    print("\nPatient:")
    print(patient.to_dict())

    print("\nValidation:")
    for n in [person, place, event, obj, emotion, date, patient]:
        print(n.type, "->", validate_node(n))

    print("\nfrom_entity() round-trip:")
    entity = {
        "id": "person_ramesh",
        "type": "PERSON",
        "name": "Ramesh",
        "relationship": "brother",
    }
    rebuilt = MemoryNode.from_entity(entity)
    print(rebuilt.to_dict())