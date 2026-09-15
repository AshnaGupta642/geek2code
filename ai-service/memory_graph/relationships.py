"""
Memory Graph Relationships

Defines the connections between nodes in the patient's memory graph.
"""

import re
from dataclasses import dataclass
from typing import Any, Dict

# ---------------------------------------------------------
# Structural relationship types
#
# These are the fixed, code-generated edge types graph_builder.py uses
# for people<->places, events<->places, etc. They are NOT the full set
# of valid relationship_type values: a PERSON -> PATIENT edge uses
# whatever relationship word came out of the patient's own story
# (BROTHER, NEIGHBOR, CHILDHOOD_FRIEND, ...), which is open-ended and
# can't be enumerated here. See validate_relationship() below.
# ---------------------------------------------------------
RELATED_TO = "RELATED_TO"
ASSOCIATED_WITH = "ASSOCIATED_WITH"
INVOLVES = "INVOLVES"
OCCURRED_AT = "OCCURRED_AT"

STRUCTURAL_RELATIONSHIP_TYPES = {RELATED_TO, ASSOCIATED_WITH, INVOLVES, OCCURRED_AT}

# A normalized relationship_type (after strip + upper) should look like
# a single token, e.g. "BROTHER" or "CHILDHOOD_FRIEND" — letters,
# digits, and underscores only.
_VALID_TYPE_PATTERN = re.compile(r"^[A-Z0-9_]+$")


@dataclass
class MemoryRelationship:
    """
    Represents a connection between two memory graph nodes.
    """

    source_id: str
    target_id: str
    relationship_type: str

    def __post_init__(self) -> None:
        self.source_id = self.source_id.strip()
        self.target_id = self.target_id.strip()
        self.relationship_type = self.relationship_type.strip().upper()

    def to_dict(self) -> Dict[str, Any]:
        """Convert relationship to dictionary format."""
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship_type": self.relationship_type,
        }


def create_relationship(
    source_id: str,
    target_id: str,
    relationship_type: str = RELATED_TO,
) -> MemoryRelationship:
    """Create a relationship between two nodes."""
    return MemoryRelationship(
        source_id=source_id,
        target_id=target_id,
        relationship_type=relationship_type,
    )


def person_related_to_person(
    person1_id: str,
    person2_id: str,
    relationship_type: str = RELATED_TO,
) -> MemoryRelationship:
    """Connect two people (e.g. with a family relationship word like SIBLING)."""
    return create_relationship(person1_id, person2_id, relationship_type)


def person_related_to_place(person_id: str, place_id: str) -> MemoryRelationship:
    """Connect a person with a place."""
    return create_relationship(person_id, place_id, ASSOCIATED_WITH)


def event_at_place(event_id: str, place_id: str) -> MemoryRelationship:
    """Connect an event with the place where it happened."""
    return create_relationship(event_id, place_id, OCCURRED_AT)


def event_involves_person(event_id: str, person_id: str) -> MemoryRelationship:
    """Connect an event with a person involved in it."""
    return create_relationship(event_id, person_id, INVOLVES)


def photo_related_to_memory(photo_id: str, memory_id: str) -> MemoryRelationship:
    """
    Connect a photo with a memory.

    NOTE: "memory" isn't currently one of the node types defined in
    nodes.py (PERSON/PLACE/EVENT/DATE/OBJECT/EMOTION/PATIENT/PHOTO).
    Like PHOTO itself, this is a placeholder for a future feature and
    isn't wired up to anything upstream yet.
    """
    return create_relationship(photo_id, memory_id, ASSOCIATED_WITH)


def validate_relationship(relationship: MemoryRelationship) -> bool:
    """
    Validate a relationship.

    A relationship is valid if source_id and target_id are non-empty
    and relationship_type is a well-formed token (letters/digits/
    underscores after normalization). Free-text relationship words
    extracted from a patient's story (BROTHER, NEIGHBOR, ...) are
    valid even though they aren't in STRUCTURAL_RELATIONSHIP_TYPES —
    that set only covers the code-generated structural edges, not the
    open-ended vocabulary of real relationship words.
    """
    if not relationship.source_id:
        return False
    if not relationship.target_id:
        return False
    if not relationship.relationship_type:
        return False
    if not _VALID_TYPE_PATTERN.match(relationship.relationship_type):
        return False
    return True


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    relationship1 = person_related_to_person("person_ramesh", "person_sita", "SIBLING")
    relationship2 = person_related_to_place("person_ramesh", "place_shillong")
    relationship3 = event_at_place("event_wedding", "place_shillong")
    relationship4 = event_involves_person("event_wedding", "person_ramesh")

    print("Relationship 1:")
    print(relationship1.to_dict())
    print("\nRelationship 2:")
    print(relationship2.to_dict())
    print("\nRelationship 3:")
    print(relationship3.to_dict())
    print("\nRelationship 4:")
    print(relationship4.to_dict())

    print("\nValidation:")
    print(validate_relationship(relationship1))
    print(validate_relationship(relationship2))
    print(validate_relationship(relationship3))
    print(validate_relationship(relationship4))