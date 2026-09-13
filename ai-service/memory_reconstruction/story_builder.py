"""
Memory Reconstruction Story Builder

Builds a simple reconstructed personal story from the
information recalled by the patient.
"""

import logging
from typing import Any, Dict, List

try:
    from .memory_state import MemoryState
except ImportError:
    # Fallback for running this file directly (e.g. PyCharm's Run button),
    # where Python has no parent package to resolve the leading "."
    # against. Requires memory_state.py to be in the same folder.
    from memory_state import MemoryState

logger = logging.getLogger(__name__)

LIST_MEMORY_FIELDS = ("places", "events", "dates", "objects", "emotions")


class StoryBuilder:
    """Build a reconstructed story from patient recall."""

    def __init__(self) -> None:
        pass

    # ---------------------------------------------------------
    # Build story
    # ---------------------------------------------------------

    def build_story(
        self,
        state: MemoryState,
        original_memory: Dict[str, Any],
    ) -> str:
        """
        Build a simple story from the patient's recalled information.

        Args:
            state:
                Current reconstruction state.

            original_memory:
                Original structured memory. Used to ground the story:
                anything in state.recalled_information that can't be
                verified against original_memory is dropped rather than
                stated back to the patient as fact. This matters more
                once an LLM sits in front of this (reconstruction_engine
                + llm_client) — free-form generation raises the risk of
                something ungrounded ending up in recalled_information.

        Returns:
            Reconstructed story as text.
        """

        if not isinstance(original_memory, dict):
            raise ValueError("original_memory must be a dictionary")

        recalled = self._grounded_recall(
            state.recalled_information, original_memory
        )

        if not recalled:
            return (
                "We could not reconstruct enough details "
                "from this memory yet."
            )

        parts: List[str] = []

        # -----------------------------------------------------
        # People
        # -----------------------------------------------------

        people = recalled.get("people", [])

        if people:
            names = []

            for person in people:
                if isinstance(person, dict):
                    name = person.get("name", "")
                    relationship = person.get("relationship", "")

                    if name and relationship:
                        names.append(f"{name}, your {relationship}")
                    elif name:
                        names.append(name)

            if names:
                parts.append("You remember " + self._join_items(names) + ".")

        # -----------------------------------------------------
        # Places
        # -----------------------------------------------------

        places = recalled.get("places", [])

        if places:
            parts.append(
                "You remember being at " + self._join_items(places) + "."
            )

        # -----------------------------------------------------
        # Events
        # -----------------------------------------------------

        events = recalled.get("events", [])

        if events:
            parts.append("You remember " + self._join_items(events) + ".")

        # -----------------------------------------------------
        # Dates
        # -----------------------------------------------------

        dates = recalled.get("dates", [])

        if dates:
            parts.append(
                "You remember the time as " + self._join_items(dates) + "."
            )

        # -----------------------------------------------------
        # Objects
        # -----------------------------------------------------

        objects = recalled.get("objects", [])

        if objects:
            parts.append("You also remember " + self._join_items(objects) + ".")

        # -----------------------------------------------------
        # Emotions
        # -----------------------------------------------------

        emotions = recalled.get("emotions", [])

        if emotions:
            parts.append(
                "You remember feeling " + self._join_items(emotions) + "."
            )

        # -----------------------------------------------------
        # Patient's actual answers
        # -----------------------------------------------------

        answers = state.answers

        if answers:
            parts.append(
                "During our conversation, you shared: " + self._join_answers(answers)
            )

        if not parts:
            return (
                "You remembered a few details, "
                "but we need more information to tell the story."
            )

        return " ".join(parts)

    # ---------------------------------------------------------
    # Ground recalled information against the original memory
    # ---------------------------------------------------------

    def _grounded_recall(
        self,
        recalled: Dict[str, Any],
        original_memory: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Filter state.recalled_information down to only what can be
        verified against original_memory. Anything that doesn't match
        is dropped (and logged) rather than stated to the patient.
        """

        if not recalled:
            return {}

        grounded: Dict[str, Any] = {}

        # People — match by name (case-insensitive)
        people = recalled.get("people", [])

        if people:
            original_names = {
                str(p.get("name", "")).strip().lower()
                for p in original_memory.get("people", [])
                if isinstance(p, dict) and p.get("name")
            }

            kept_people = []
            dropped_people = []

            for person in people:
                if not isinstance(person, dict):
                    continue

                name = str(person.get("name", "")).strip()

                if name.lower() in original_names:
                    kept_people.append(person)
                else:
                    dropped_people.append(name)

            if dropped_people:
                logger.warning(
                    "Dropping ungrounded recalled people (not in original memory): %s",
                    dropped_people,
                )

            if kept_people:
                grounded["people"] = kept_people

        # Places / events / dates / objects / emotions — match by
        # case-insensitive string equality against the original list.
        for field in LIST_MEMORY_FIELDS:
            items = recalled.get(field, [])

            if not items:
                continue

            original_items = {
                str(item).strip().lower()
                for item in original_memory.get(field, [])
                if isinstance(item, str)
            }

            kept = [
                item
                for item in items
                if isinstance(item, str) and item.strip().lower() in original_items
            ]

            dropped = [item for item in items if item not in kept]

            if dropped:
                logger.warning(
                    "Dropping ungrounded recalled %s (not in original memory): %s",
                    field,
                    dropped,
                )

            if kept:
                grounded[field] = kept

        return grounded

    # ---------------------------------------------------------
    # Join items
    # ---------------------------------------------------------

    def _join_items(self, items: List[str]) -> str:
        """Join items naturally."""

        items = [item.strip() for item in items if item and item.strip()]

        if not items:
            return ""

        if len(items) == 1:
            return items[0]

        if len(items) == 2:
            return f"{items[0]} and {items[1]}"

        return ", ".join(items[:-1]) + ", and " + items[-1]

    # ---------------------------------------------------------
    # Join answers
    # ---------------------------------------------------------

    def _join_answers(self, answers: List[str]) -> str:
        """
        Combine patient answers into readable text.

        Ensures each answer ends with terminal punctuation before
        joining, so answers that weren't punctuated by the patient
        (or upstream capture) don't run together into one sentence.
        """

        cleaned = []

        for answer in answers:
            if not answer or not answer.strip():
                continue

            text = answer.strip()

            if text[-1] not in ".!?":
                text += "."

            cleaned.append(text)

        return " ".join(cleaned)

    # ---------------------------------------------------------
    # Build short summary
    # ---------------------------------------------------------

    def build_summary(self, state: MemoryState) -> str:
        """
        Build a short summary from recalled information.

        Note: unlike build_story(), this doesn't take original_memory
        and isn't grounded against it — it's a lightweight view meant
        for internal/debug use, not patient-facing narration.
        """

        recalled = state.recalled_information

        summary_parts = []

        people = recalled.get("people", [])
        places = recalled.get("places", [])
        events = recalled.get("events", [])

        if people:
            names = []

            for person in people:
                if isinstance(person, dict):
                    name = person.get("name", "")

                    if name:
                        names.append(name)

            if names:
                summary_parts.append("People: " + self._join_items(names))

        if places:
            summary_parts.append("Places: " + self._join_items(places))

        if events:
            summary_parts.append("Events: " + self._join_items(events))

        if not summary_parts:
            return "No major details were recalled yet."

        return " | ".join(summary_parts)


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    state = MemoryState(patient_id="P001", memory_id="M001")

    # Simulate information recalled by the patient
    state.add_recalled_information(
        "people", [{"name": "Ramesh", "relationship": "brother"}]
    )
    state.add_recalled_information("places", ["Shillong", "Ward's Lake"])
    state.add_recalled_information("events", ["a family trip"])
    state.add_recalled_information("emotions", ["happy"])

    state.add_answer("I went to Shillong with my brother Ramesh")
    state.add_answer("We visited Ward's Lake and had a good time.")

    original_memory = {
        "people": [{"name": "Ramesh", "relationship": "brother"}],
        "places": ["Shillong", "Ward's Lake"],
        "events": ["a family trip"],
    }

    builder = StoryBuilder()

    story = builder.build_story(state, original_memory)
    summary = builder.build_summary(state)

    print("\nRECONSTRUCTED STORY")
    print("=" * 60)
    print(story)

    print("\nSHORT SUMMARY")
    print("=" * 60)
    print(summary)

    # ---------------------------------------------------------
    # Grounding test: an ungrounded item should be dropped, not
    # stated back to the patient as fact.
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("GROUNDING TEST — fabricated place should be dropped")
    print("=" * 60)

    state2 = MemoryState(patient_id="P002", memory_id="M002")
    state2.add_recalled_information(
        "places", ["Shillong", "Narnia"]  # "Narnia" isn't in original_memory
    )
    state2.add_answer("We went to Shillong, and maybe Narnia too?")

    story2 = builder.build_story(state2, original_memory)
    print(story2)