"""
Memory Graph Builder

Builds a graph from entities extracted from a patient's memory.

This file coordinates:
    - nodes.py
    - relationships.py

Example:

Ramesh ── BROTHER ──> Patient
Ramesh ── ASSOCIATED_WITH ──> Shillong
Sunday Visit ── OCCURRED_AT ──> Shillong
Sunday Visit ── INVOLVES ──> Ramesh
Blue school bag ── ASSOCIATED_WITH ──> Sunday Visit
Happy ── ASSOCIATED_WITH ──> Sunday Visit
"""

import logging
from typing import Any, Dict, List, Optional

try:
    # Normal case: graph_builder.py is imported as part of the
    # memory_graph package (e.g. `python -m memory_graph.graph_builder`,
    # or imported from elsewhere as `from memory_graph.graph_builder
    # import GraphBuilder`).
    from .nodes import (
        MemoryNode,
        create_person_node,
        create_place_node,
        create_event_node,
        create_photo_node,
        create_object_node,
        create_emotion_node,
        create_date_node,
        create_patient_node,
    )
    from .relationships import (
        MemoryRelationship,
        create_relationship,
    )
except ImportError:
    # Fallback for running this file directly (e.g. PyCharm's Run button,
    # `python graph_builder.py`), where Python has no parent package to
    # resolve the leading "." against. Requires nodes.py and
    # relationships.py to be on the path (they are, since they're in the
    # same folder and this file's own directory is added to sys.path
    # automatically when run as a script).
    from nodes import (
        MemoryNode,
        create_person_node,
        create_place_node,
        create_event_node,
        create_photo_node,
        create_object_node,
        create_emotion_node,
        create_date_node,
        create_patient_node,
    )
    from relationships import (
        MemoryRelationship,
        create_relationship,
    )

logger = logging.getLogger(__name__)

PATIENT_NODE_ID = "patient"


class GraphBuilder:
    """Build a memory graph from memory entities."""

    def __init__(self) -> None:
        pass

    # ---------------------------------------------------------
    # Build complete graph
    # ---------------------------------------------------------

    def build_graph(
        self,
        entities: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Build graph nodes and relationships.

        Args:
            entities:
                Graph-ready entities from entity_extractor.py.

        Returns:
            Dictionary containing nodes and relationships.
        """

        if not isinstance(entities, list):
            raise ValueError("entities must be a list")

        nodes = self._build_nodes(entities)
        relationships = self._build_relationships(entities)

        logger.info(
            "Built graph: %d nodes, %d relationships",
            len(nodes),
            len(relationships),
        )

        return {
            "nodes": nodes,
            "relationships": relationships,
        }

    # ---------------------------------------------------------
    # Build nodes
    # ---------------------------------------------------------

    def _build_nodes(
        self,
        entities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Convert entities into graph nodes.

        A Patient node is always included because relationships
        can point to the patient.
        """

        nodes: List[Dict[str, Any]] = []

        # Always add Patient node, via the shared factory in nodes.py
        # so its shape can't drift out of sync with how PATIENT nodes
        # are built anywhere else.
        patient_node = create_patient_node(patient_id=PATIENT_NODE_ID)
        nodes.append(patient_node.to_dict())

        seen_ids = {PATIENT_NODE_ID}

        for entity in entities:

            if not isinstance(entity, dict):
                continue

            entity_id = entity.get("id")
            entity_type = str(entity.get("type", "")).upper()
            name = entity.get("name")
            relationship = entity.get("relationship", "")

            if not entity_id or not entity_type or not name:
                continue

            if entity_id in seen_ids:
                continue

            # Create appropriate node type
            node = self._create_node(
                entity_id=entity_id,
                entity_type=entity_type,
                name=str(name),
                relationship=str(relationship),
            )

            if node is None:
                logger.warning(
                    "Unsupported entity type: %s",
                    entity_type,
                )
                continue

            nodes.append(node.to_dict())
            seen_ids.add(entity_id)

        return nodes

    # ---------------------------------------------------------
    # Create individual node
    # ---------------------------------------------------------

    def _create_node(
        self,
        entity_id: str,
        entity_type: str,
        name: str,
        relationship: str = "",
    ) -> Optional[MemoryNode]:
        """
        Create a MemoryNode using the appropriate helper
        from nodes.py.
        """

        if entity_type == "PERSON":

            return create_person_node(
                person_id=entity_id,
                name=name,
                relationship=relationship,
            )

        if entity_type == "PLACE":

            return create_place_node(
                place_id=entity_id,
                name=name,
            )

        if entity_type == "EVENT":

            return create_event_node(
                event_id=entity_id,
                name=name,
            )

        if entity_type == "PHOTO":

            return create_photo_node(
                photo_id=entity_id,
                label=name,
            )

        if entity_type == "OBJECT":

            return create_object_node(
                object_id=entity_id,
                name=name,
            )

        if entity_type == "EMOTION":

            return create_emotion_node(
                emotion_id=entity_id,
                name=name,
            )

        if entity_type == "DATE":

            return create_date_node(
                date_id=entity_id,
                label=name,
            )

        return None

    # ---------------------------------------------------------
    # Build relationships
    # ---------------------------------------------------------

    def _build_relationships(
        self,
        entities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Create relationships between graph entities.

        Relationships are created using the helper functions
        from relationships.py.
        """

        by_type: Dict[str, List[Dict[str, Any]]] = {
            "PERSON": [],
            "PLACE": [],
            "EVENT": [],
            "PHOTO": [],
            "OBJECT": [],
            "EMOTION": [],
            "DATE": [],
        }

        for entity in entities:

            if not isinstance(entity, dict):
                continue

            entity_type = str(
                entity.get("type", "")
            ).upper()

            if entity_type in by_type:
                by_type[entity_type].append(entity)

        people = by_type["PERSON"]
        places = by_type["PLACE"]
        events = by_type["EVENT"]
        photos = by_type["PHOTO"]
        objects = by_type["OBJECT"]
        emotions = by_type["EMOTION"]
        dates = by_type["DATE"]

        relationships: List[MemoryRelationship] = []

        # -----------------------------------------------------
        # Person -> Patient
        # -----------------------------------------------------

        for person in people:

            person_relationship = str(
                person.get("relationship", "")
            ).strip()

            if not person_relationship:
                continue

            relationships.append(
                create_relationship(
                    source_id=person["id"],
                    target_id=PATIENT_NODE_ID,
                    relationship_type=person_relationship.upper(),
                )
            )

        # -----------------------------------------------------
        # People -> Places
        # -----------------------------------------------------

        for person in people:
            for place in places:
                relationships.append(
                    create_relationship(
                        source_id=person["id"],
                        target_id=place["id"],
                        relationship_type="ASSOCIATED_WITH",
                    )
                )

        # -----------------------------------------------------
        # Events -> Places
        # -----------------------------------------------------

        for event in events:
            for place in places:
                relationships.append(
                    create_relationship(
                        source_id=event["id"],
                        target_id=place["id"],
                        relationship_type="OCCURRED_AT",
                    )
                )

        # -----------------------------------------------------
        # Events -> People
        # -----------------------------------------------------

        for event in events:
            for person in people:
                relationships.append(
                    create_relationship(
                        source_id=event["id"],
                        target_id=person["id"],
                        relationship_type="INVOLVES",
                    )
                )

        # -----------------------------------------------------
        # Photos -> Events
        # -----------------------------------------------------

        for photo in photos:
            for event in events:
                relationships.append(
                    create_relationship(
                        source_id=photo["id"],
                        target_id=event["id"],
                        relationship_type="ASSOCIATED_WITH",
                    )
                )

        # -----------------------------------------------------
        # Objects -> Events
        # -----------------------------------------------------

        for obj in objects:
            for event in events:
                relationships.append(
                    create_relationship(
                        source_id=obj["id"],
                        target_id=event["id"],
                        relationship_type="ASSOCIATED_WITH",
                    )
                )

        # -----------------------------------------------------
        # Emotions -> Events
        # -----------------------------------------------------

        for emotion in emotions:
            for event in events:
                relationships.append(
                    create_relationship(
                        source_id=emotion["id"],
                        target_id=event["id"],
                        relationship_type="ASSOCIATED_WITH",
                    )
                )

        # -----------------------------------------------------
        # Dates -> Events
        # -----------------------------------------------------

        for date in dates:
            for event in events:
                relationships.append(
                    create_relationship(
                        source_id=date["id"],
                        target_id=event["id"],
                        relationship_type="ASSOCIATED_WITH",
                    )
                )

        edge_dicts = [edge.to_dict() for edge in relationships]

        return self._remove_duplicate_relationships(edge_dicts)

    # ---------------------------------------------------------
    # Remove duplicate relationships
    # ---------------------------------------------------------

    def _remove_duplicate_relationships(
        self,
        relationships: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Remove duplicate graph relationships.
        """

        unique: List[Dict[str, Any]] = []
        seen = set()

        for relationship in relationships:

            key = (
                relationship["source_id"],
                relationship["target_id"],
                relationship["relationship_type"],
            )

            if key in seen:
                continue

            seen.add(key)
            unique.append(relationship)

        return unique


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    builder = GraphBuilder()

    entities = [
        {"id": "person_ramesh", "type": "PERSON", "name": "Ramesh", "relationship": "brother"},
        {"id": "person_sita", "type": "PERSON", "name": "Sita", "relationship": "sister"},
        {"id": "place_shillong", "type": "PLACE", "name": "Shillong"},
        {"id": "place_ward_s_lake", "type": "PLACE", "name": "Ward's Lake"},
        {"id": "event_sunday_visit", "type": "EVENT", "name": "Sunday visit to Ward's Lake"},
        {"id": "photo_family", "type": "PHOTO", "name": "Family photo"},
        {"id": "object_school_bag", "type": "OBJECT", "name": "Blue school bag"},
        {"id": "emotion_happy", "type": "EMOTION", "name": "Happy"},
        {"id": "date_1998", "type": "DATE", "name": "1998"},
    ]

    graph = builder.build_graph(entities)

    print("\n" + "=" * 60)
    print("NODES")
    print("=" * 60)
    for node in graph["nodes"]:
        print(node)

    print("\n" + "=" * 60)
    print("RELATIONSHIPS")
    print("=" * 60)
    for relationship in graph["relationships"]:
        print(
            f"{relationship['source_id']} "
            f"── {relationship['relationship_type']} ──> "
            f"{relationship['target_id']}"
        )
    print("=" * 60)