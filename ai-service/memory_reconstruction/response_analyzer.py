"""
Memory Reconstruction Response Analyzer

Analyzes a patient's answer during memory reconstruction.

The analyzer:
1. Checks whether the patient gave a meaningful answer.
2. Identifies information recalled from the memory.
3. Detects uncertainty or lack of recall.
4. Returns structured information for MemoryState.
"""

import re
from typing import Any, Dict, List, Tuple

# Fields scanned for simple (non-people) list matches, in output order.
LIST_MEMORY_FIELDS = ("places", "events", "dates", "objects", "emotions")


class ResponseAnalyzer:
    """Analyze patient responses during memory reconstruction."""

    # ---------------------------------------------------------
    # Main analysis
    # ---------------------------------------------------------

    def analyze_response(
        self,
        response: str,
        memory: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze the patient's response.

        Args:
            response:
                Patient's answer.

            memory:
                Structured memory containing known information.

        Returns:
            Analysis dictionary.
        """

        if not isinstance(response, str):
            raise ValueError("response must be a string")

        if not isinstance(memory, dict):
            raise ValueError("memory must be a dictionary")

        response = response.strip()

        if not response:
            return {
                "meaningful": False,
                "recall_detected": False,
                "recalled_information": {},
                "matched_memory": [],
                "confidence": 0.0,
                "needs_support": True,
            }

        # Detect uncertainty / lack of recall (hedge words like "maybe")
        uncertain = self._detect_uncertainty(response)

        # Find information from the known memory (single pass, shared
        # by both the flat match list and the structured recalled info)
        matched_memory, recalled_information = self._match_memory(
            response.lower(), memory
        )

        if matched_memory:
            confidence = min(1.0, 0.5 + (0.15 * len(matched_memory)))
        elif uncertain:
            confidence = 0.1
        else:
            confidence = 0.3

        # A response that actually recalled something real is meaningful
        # even if it's hedged ("maybe we went to Shillong"). Only treat
        # it as needing support when there's uncertainty AND nothing was
        # actually recalled — otherwise a partially-hedged but correct
        # answer would be flagged as both "recalled" and "not meaningful",
        # which is contradictory and would make downstream prompting
        # respond as if the patient recalled nothing.
        meaningful = bool(matched_memory) or not uncertain
        needs_support = uncertain and not matched_memory

        return {
            "meaningful": meaningful,
            "recall_detected": bool(matched_memory),
            "recalled_information": recalled_information,
            "matched_memory": matched_memory,
            "confidence": round(confidence, 2),
            "needs_support": needs_support,
        }

    # ---------------------------------------------------------
    # Detect uncertainty
    # ---------------------------------------------------------

    def _detect_uncertainty(self, response: str) -> bool:
        """
        Detect phrases suggesting that the patient
        does not remember or is unsure.
        """

        uncertainty_phrases = [
            "i don't know",
            "i dont know",
            "i don't remember",
            "i dont remember",
            "can't remember",
            "cant remember",
            "not sure",
            "i'm not sure",
            "im not sure",
            "i forgot",
            "no idea",
            "maybe",
            "perhaps",
        ]

        response_lower = response.lower()

        return any(phrase in response_lower for phrase in uncertainty_phrases)

    # ---------------------------------------------------------
    # Phrase matching (word-boundary aware)
    # ---------------------------------------------------------

    def _contains_phrase(self, response_lower: str, phrase: str) -> bool:
        """
        Check whether `phrase` appears in `response_lower` as a whole
        word/phrase, not as a substring of a larger word.

        Plain `phrase in text` matching would let a relationship like
        "son" match inside "person" or "season", or a place like "India"
        match inside "Indiana" — inflating matched_memory/confidence
        with things the patient never actually said.
        """

        phrase_lower = phrase.lower().strip()
        if not phrase_lower:
            return False

        pattern = r"(?<!\w)" + re.escape(phrase_lower) + r"(?!\w)"
        return re.search(pattern, response_lower) is not None

    # ---------------------------------------------------------
    # Find + extract matched memory in one pass
    # ---------------------------------------------------------

    def _match_memory(
        self,
        response_lower: str,
        memory: Dict[str, Any],
    ) -> Tuple[List[str], Dict[str, Any]]:
        """
        Scan the response once against known memory information.

        Returns:
            (matches, recalled_information) where `matches` is a flat,
            deduplicated list of everything mentioned, and
            `recalled_information` groups the same hits by category
            (mirroring the shape of the structured memory).
        """

        matches: List[str] = []
        recalled: Dict[str, Any] = {}

        # People (name and/or relationship, tracked separately in
        # `matches` but grouped together per-person in `recalled`)
        recalled_people = []

        for person in memory.get("people", []):
            if not isinstance(person, dict):
                continue

            name = str(person.get("name", "")).strip()
            relationship = str(person.get("relationship", "")).strip()

            name_hit = bool(name) and self._contains_phrase(response_lower, name)
            relationship_hit = bool(relationship) and self._contains_phrase(
                response_lower, relationship
            )

            if name_hit:
                matches.append(name)
            if relationship_hit:
                matches.append(relationship)

            if name_hit or relationship_hit:
                recalled_people.append({"name": name, "relationship": relationship})

        if recalled_people:
            recalled["people"] = recalled_people

        # Places, events, dates, objects, emotions
        for field in LIST_MEMORY_FIELDS:
            hits = self._match_list(response_lower, memory.get(field, []))
            if hits:
                matches.extend(hits)
                recalled[field] = hits

        # Deduplicate the flat match list while preserving order
        unique_matches: List[str] = []
        for item in matches:
            if item not in unique_matches:
                unique_matches.append(item)

        return unique_matches, recalled

    def _match_list(self, response_lower: str, items: Any) -> List[str]:
        """Return memory items from a plain string list mentioned in the response."""

        if not isinstance(items, list):
            return []

        hits = []
        for item in items:
            if not isinstance(item, str):
                continue

            item = item.strip()
            if item and self._contains_phrase(response_lower, item):
                hits.append(item)

        return hits


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":

    analyzer = ResponseAnalyzer()

    memory = {
        "people": [
            {"name": "Ramesh", "relationship": "brother"},
            {"name": "Sita", "relationship": "sister"},
        ],
        "places": ["Shillong", "Ward's Lake"],
        "events": ["family trip"],
        "dates": ["Sunday"],
        "objects": ["blue school bag"],
        "emotions": ["happy"],
    }

    # Test 1: clear recall
    response1 = "Yes, I remember Ramesh. He is my brother. We went to Shillong."
    result1 = analyzer.analyze_response(response1, memory)
    print("\nTEST 1 — clear recall")
    print("=" * 50)
    print(result1)

    # Test 2: no recall, expresses uncertainty
    response2 = "I don't remember."
    result2 = analyzer.analyze_response(response2, memory)
    print("\nTEST 2 — no recall, uncertain")
    print("=" * 50)
    print(result2)

    # Test 3: clear recall, multiple items
    response3 = "We went to Ward's Lake on Sunday and I felt happy."
    result3 = analyzer.analyze_response(response3, memory)
    print("\nTEST 3 — multiple matches")
    print("=" * 50)
    print(result3)

    # Test 4: hedged but real recall — should be meaningful, not need support
    response4 = "Maybe it was Shillong, we went there on Sunday."
    result4 = analyzer.analyze_response(response4, memory)
    print("\nTEST 4 — hedged but real recall (meaningful should be True)")
    print("=" * 50)
    print(result4)

    # Test 5: substring false-positive check — "person" should NOT match "son"
    memory_with_son = {
        "people": [{"name": "Arjun", "relationship": "son"}],
        "places": [],
        "events": [],
        "dates": [],
        "objects": [],
        "emotions": [],
    }
    response5 = "That person looks familiar but I can't place them."
    result5 = analyzer.analyze_response(response5, memory_with_son)
    print("\nTEST 5 — 'son' should NOT match inside 'person'")
    print("=" * 50)
    print(result5)