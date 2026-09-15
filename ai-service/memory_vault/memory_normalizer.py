"""
Memory Normalizer

Cleans and standardizes memory data before it is sent
to the Memory Graph.
"""

import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class MemoryNormalizer:
    """Normalize structured memory and graph entities."""

    # ---------------------------------------------------------
    # Normalize complete memory
    # ---------------------------------------------------------

    def normalize_memory(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean the output of memory_extractor.py.
        """
        if not isinstance(memory, dict):
            raise ValueError("memory must be a dictionary")

        result = {
            "people": self._normalize_people(memory.get("people", [])),
            "places": self._normalize_list(memory.get("places", [])),
            "events": self._normalize_list(memory.get("events", [])),
            "dates": self._normalize_list(memory.get("dates", [])),
            "objects": self._normalize_list(memory.get("objects", [])),
            "emotions": self._normalize_list(memory.get("emotions", [])),
            "summary": self._clean_text(memory.get("summary", "")),
        }

        logger.info(
            "Normalized memory: %d people, %d places, %d events",
            len(result["people"]),
            len(result["places"]),
            len(result["events"]),
        )

        return result

    # ---------------------------------------------------------
    # Normalize people
    # ---------------------------------------------------------

    def _normalize_people(self, people: List[Any]) -> List[Dict[str, str]]:
        """
        Clean people information and merge duplicates by name.
        If the same person appears twice with different relationship
        values, the non-empty relationship is kept rather than
        arbitrarily keeping whichever entry came first.
        """
        if not isinstance(people, list):
            return []

        merged: Dict[str, Dict[str, str]] = {}

        for person in people:
            if not isinstance(person, dict):
                continue

            name = self._clean_text(person.get("name", ""))
            relationship = self._clean_text(person.get("relationship", ""))

            if not name:
                continue

            key = name.lower()

            if key not in merged:
                merged[key] = {"name": name, "relationship": relationship}
            elif not merged[key]["relationship"] and relationship:
                merged[key]["relationship"] = relationship

        return list(merged.values())

    # ---------------------------------------------------------
    # Normalize lists
    # ---------------------------------------------------------

    def _normalize_list(self, items: Any) -> List[str]:
        """
        Clean a list of values into strings and remove duplicates.
        Scalar non-string items (e.g. numbers) are coerced to text
        rather than silently dropped; dicts/lists are skipped since
        they have no meaningful plain-text form here.
        """
        if not isinstance(items, list):
            return []

        normalized = []
        seen = set()

        for item in items:
            if isinstance(item, (dict, list)):
                continue

            cleaned = self._clean_text(item)
            if not cleaned:
                continue

            key = cleaned.lower()
            if key in seen:
                continue

            seen.add(key)
            normalized.append(cleaned)

        return normalized

    # ---------------------------------------------------------
    # Clean text
    # ---------------------------------------------------------

    def _clean_text(self, text: Any) -> str:
        """Clean spaces and unnecessary characters."""
        if text is None:
            return ""

        text = str(text).strip()
        text = re.sub(r"\s+", " ", text)

        return text

    # ---------------------------------------------------------
    # Normalize graph entities
    # ---------------------------------------------------------

    def normalize_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize entities produced by entity_extractor.py, merging
        duplicate IDs instead of dropping later, potentially richer
        entries (e.g. a PERSON's relationship filled in on a later mention).
        """
        if not isinstance(entities, list):
            return []

        merged: Dict[str, Dict[str, Any]] = {}

        for entity in entities:
            if not isinstance(entity, dict):
                continue

            entity_id = self._clean_text(entity.get("id", ""))
            entity_type = self._clean_text(entity.get("type", "")).upper()
            name = self._clean_text(entity.get("name", ""))

            if not entity_id or not entity_type or not name:
                continue

            clean_entity: Dict[str, Any] = {
                "id": entity_id,
                "type": entity_type,
                "name": name,
            }

            if entity_type == "PERSON":
                clean_entity["relationship"] = self._clean_text(entity.get("relationship", ""))

            if entity_id not in merged:
                merged[entity_id] = clean_entity
            elif entity_type == "PERSON" and not merged[entity_id].get("relationship"):
                if clean_entity.get("relationship"):
                    merged[entity_id]["relationship"] = clean_entity["relationship"]

        result = list(merged.values())
        logger.info("Normalized %d graph entities", len(result))

        return result


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    normalizer = MemoryNormalizer()

    memory = {
        "people": [
            {"name": "  Ramesh  ", "relationship": " brother "},
            {"name": "Ramesh", "relationship": ""},
        ],
        "places": [" Shillong ", "Ward's Lake", "shillong"],
        "events": ["Going to Ward's Lake every Sunday"],
        "dates": [],
        "objects": [" blue school bag "],
        "emotions": [" happy ", "happy"],
        "summary": "  The patient remembers living in Shillong.  ",
    }

    result = normalizer.normalize_memory(memory)

    print("\nNormalized Memory:\n")
    print(result)

    entities = [
        {"id": "person_ramesh", "type": "person", "name": " Ramesh "},
        {"id": "place_shillong", "type": "place", "name": " Shillong "},
        {"id": "place_shillong", "type": "place", "name": "shillong"},
    ]

    normalized_entities = normalizer.normalize_entities(entities)

    print("\nNormalized Entities:\n")
    for entity in normalized_entities:
        print(entity)