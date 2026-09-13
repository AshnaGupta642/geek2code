"""
Entity Extractor

Converts structured memory information into graph-ready entities.

Input:
    Output from MemoryExtractor

Output:
    A list of uniquely identified entities that can later
    be used by the Memory Graph.
"""

import hashlib
import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class EntityExtractor:
    """Convert structured memory into graph-ready entities (no API calls)."""

    def __init__(self) -> None:
        pass

    # ---------------------------------------------------------
    # Main function
    # ---------------------------------------------------------

    def extract_entities(self, memory: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Convert structured memory into graph entities.

        Args:
            memory: Structured memory returned by memory_extractor.py.

        Returns:
            Dictionary containing graph-ready entities, deduplicated by ID.
        """
        if not isinstance(memory, dict):
            raise ValueError("memory must be a dictionary")

        entities: List[Dict[str, Any]] = []

        # People
        for person in memory.get("people", []):
            if not isinstance(person, dict):
                continue
            name = str(person.get("name", "")).strip()
            if not name:
                continue
            relationship = str(person.get("relationship", "")).strip()
            entities.append(
                {
                    "id": self._make_id("person", name),
                    "type": "PERSON",
                    "name": name,
                    "relationship": relationship,
                }
            )

        # Places
        for place in memory.get("places", []):
            place = str(place).strip()
            if not place:
                continue
            entities.append(
                {"id": self._make_id("place", place), "type": "PLACE", "name": place}
            )

        # Events
        for event in memory.get("events", []):
            event = str(event).strip()
            if not event:
                continue
            entities.append(
                {"id": self._make_id("event", event), "type": "EVENT", "name": event}
            )

        # Dates
        for date in memory.get("dates", []):
            date = str(date).strip()
            if not date:
                continue
            entities.append(
                {"id": self._make_id("date", date), "type": "DATE", "name": date}
            )

        # Objects
        for obj in memory.get("objects", []):
            obj = str(obj).strip()
            if not obj:
                continue
            entities.append(
                {"id": self._make_id("object", obj), "type": "OBJECT", "name": obj}
            )

        # Emotions
        for emotion in memory.get("emotions", []):
            emotion = str(emotion).strip()
            if not emotion:
                continue
            entities.append(
                {"id": self._make_id("emotion", emotion), "type": "EMOTION", "name": emotion}
            )

        entities = self._merge_duplicates(entities)

        logger.info("Extracted %d graph-ready entities", len(entities))

        return {"entities": entities}

    # ---------------------------------------------------------
    # Create entity ID
    # ---------------------------------------------------------

    def _make_id(self, entity_type: str, name: str) -> str:
        """
        Create a stable ID.

        Example:
            person + Ramesh -> person_ramesh

        If the name normalizes to nothing usable (e.g. "???" or emoji-only
        text), falls back to a short hash of the original name so unrelated
        entities never accidentally collide on the same empty ID.
        """
        clean_name = name.lower().strip()
        clean_name = re.sub(r"[^a-z0-9]+", "_", clean_name)
        clean_name = clean_name.strip("_")

        if not clean_name:
            clean_name = hashlib.sha1(name.encode("utf-8")).hexdigest()[:8]

        return f"{entity_type}_{clean_name}"

    # ---------------------------------------------------------
    # Merge duplicates (instead of silently dropping)
    # ---------------------------------------------------------

    def _merge_duplicates(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Merge entities with duplicate IDs instead of just dropping later ones.
        For PERSON entities, if an earlier entry has an empty `relationship`
        and a later one has a real value (or vice versa), the non-empty
        value is kept rather than losing that information.
        """
        merged: Dict[str, Dict[str, Any]] = {}

        for entity in entities:
            entity_id = entity["id"]

            if entity_id not in merged:
                merged[entity_id] = entity
                continue

            existing = merged[entity_id]
            if entity.get("type") == "PERSON" and not existing.get("relationship"):
                if entity.get("relationship"):
                    existing["relationship"] = entity["relationship"]

        return list(merged.values())


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    extractor = EntityExtractor()

    # This represents the output from memory_extractor.py
    memory = {
        "people": [{"name": "Ramesh", "relationship": "brother"}],
        "places": ["Shillong", "Ward's Lake"],
        "events": ["Going to Ward's Lake every Sunday"],
        "dates": [],
        "objects": ["blue school bag"],
        "emotions": ["happy"],
        "summary": "The patient lived in Shillong with their brother Ramesh.",
    }

    result = extractor.extract_entities(memory)

    print("\nGraph-ready entities:\n")
    for entity in result["entities"]:
        print(entity)