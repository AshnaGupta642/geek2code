"""
Memory Reconstruction State

Keeps track of a patient's progress while reconstructing
a personal memory.

Reconstruction stages:

1. Recognition
2. Association
3. Context
4. Event
5. Story
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


# ---------------------------------------------------------
# Reconstruction stages
# ---------------------------------------------------------

RECOGNITION = 1
ASSOCIATION = 2
CONTEXT = 3
EVENT = 4
STORY = 5

MIN_STAGE = RECOGNITION
MAX_STAGE = STORY

STAGE_NAMES = {
    RECOGNITION: "Recognition",
    ASSOCIATION: "Association",
    CONTEXT: "Context",
    EVENT: "Event",
    STORY: "Story",
}


# ---------------------------------------------------------
# Memory Reconstruction State
# ---------------------------------------------------------

@dataclass
class MemoryState:
    """
    Stores the current state of a memory reconstruction session.
    """

    patient_id: str
    memory_id: str

    # Current reconstruction stage
    stage: int = RECOGNITION

    # Number of prompts asked
    prompt_count: int = 0

    # Answers given by the patient
    answers: List[str] = field(default_factory=list)

    # Prompts already shown to the patient
    prompts: List[str] = field(default_factory=list)

    # Information successfully recalled
    recalled_information: Dict[str, Any] = field(default_factory=dict)

    # Whether reconstruction is complete
    completed: bool = False

    def __post_init__(self) -> None:
        self.patient_id = self.patient_id.strip()
        self.memory_id = self.memory_id.strip()
        if not self.patient_id:
            raise ValueError("MemoryState.patient_id cannot be empty.")
        if not self.memory_id:
            raise ValueError("MemoryState.memory_id cannot be empty.")

    # -----------------------------------------------------
    # Add prompt
    # -----------------------------------------------------

    def add_prompt(self, prompt: str) -> None:
        """Store a prompt that was shown to the patient."""
        if not prompt or not prompt.strip():
            return

        self.prompts.append(prompt.strip())
        self.prompt_count += 1

    # -----------------------------------------------------
    # Add answer
    # -----------------------------------------------------

    def add_answer(self, answer: str) -> None:
        """Store the patient's answer."""
        if not answer or not answer.strip():
            return

        self.answers.append(answer.strip())

    # -----------------------------------------------------
    # Store recalled information
    # -----------------------------------------------------

    def add_recalled_information(self, key: str, value: Any) -> None:
        """
        Store information successfully recalled by the patient.

        If this key already holds a list (e.g. "places" recalled in an
        earlier stage) and the new value is also a list, the two are
        merged/deduplicated rather than one overwriting the other — a
        patient recalling more places in a later stage shouldn't erase
        what they recalled earlier. Any other value type (e.g. a plain
        string under a one-off key) keeps simple overwrite behavior.

        Example (category-keyed, as produced by response_analyzer.py):
            key = "places"
            value = ["Shillong", "Ward's Lake"]

        Example (single key/value):
            key = "summary_note"
            value = "Patient seemed happy discussing this memory."
        """
        if not key or not key.strip():
            return

        key = key.strip()
        existing = self.recalled_information.get(key)

        if isinstance(existing, list) and isinstance(value, list):
            self.recalled_information[key] = self._merge_recalled_lists(
                existing, value
            )
            return

        self.recalled_information[key] = value

    @staticmethod
    def _merge_recalled_lists(existing: List[Any], new: List[Any]) -> List[Any]:
        """
        Merge two recalled-information lists without losing or
        duplicating data.

        - Dict items (e.g. people: [{"name": ..., "relationship": ...}])
          are merged by "name": a repeated mention fills in a missing
          field (e.g. relationship) rather than creating a duplicate
          entry.
        - Plain items (e.g. place/event strings) are merged with
          case-insensitive de-duplication, preserving first-seen order
          and original casing.
        """
        combined = existing + new

        if combined and all(isinstance(item, dict) for item in combined):
            merged: Dict[str, Dict[str, Any]] = {}
            order: List[str] = []

            for item in combined:
                name_key = str(item.get("name", "")).strip().lower()
                if not name_key:
                    continue

                if name_key not in merged:
                    merged[name_key] = dict(item)
                    order.append(name_key)
                else:
                    for field_name, field_value in item.items():
                        if field_value and not merged[name_key].get(field_name):
                            merged[name_key][field_name] = field_value

            return [merged[k] for k in order]

        merged_list: List[Any] = []
        seen = set()

        for item in combined:
            dedupe_key = item.strip().lower() if isinstance(item, str) else item
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            merged_list.append(item)

        return merged_list

    # -----------------------------------------------------
    # Move to next stage
    # -----------------------------------------------------

    def next_stage(self) -> None:
        """
        Move the reconstruction to the next stage.

        If the patient is already at the final stage (Story), this call
        marks reconstruction as completed rather than advancing stage
        further — stage stays at MAX_STAGE, but `completed` distinguishes
        "currently working through Story" from "Story stage finished."
        Callers (e.g. reconstruction_engine.py) should check
        `is_completed()` rather than assuming stage alone tells them
        whether the session is done.
        """
        if self.completed:
            return

        if self.stage < MAX_STAGE:
            self.stage += 1
        else:
            self.completed = True

    # -----------------------------------------------------
    # Get current stage name
    # -----------------------------------------------------

    def get_stage_name(self) -> str:
        """Return the name of the current reconstruction stage."""
        return STAGE_NAMES.get(self.stage, "Unknown")

    # -----------------------------------------------------
    # Check completion
    # -----------------------------------------------------

    def is_completed(self) -> bool:
        """Return True if reconstruction is complete."""
        return self.completed

    # -----------------------------------------------------
    # Convert to dictionary
    # -----------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the current state into a dictionary.

        Useful when sending state to another service/backend.
        """
        return {
            "patient_id": self.patient_id,
            "memory_id": self.memory_id,
            "stage": self.stage,
            "stage_name": self.get_stage_name(),
            "prompt_count": self.prompt_count,
            "prompts": self.prompts,
            "answers": self.answers,
            "recalled_information": self.recalled_information,
            "completed": self.completed,
        }

    # -----------------------------------------------------
    # Reset session
    # -----------------------------------------------------

    def reset(self) -> None:
        """
        Reset the reconstruction session.

        Note: patient_id and memory_id are intentionally left unchanged —
        this resets *progress* on the same memory, not the session's
        identity.
        """
        self.stage = RECOGNITION
        self.prompt_count = 0
        self.answers.clear()
        self.prompts.clear()
        self.recalled_information.clear()
        self.completed = False


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":

    state = MemoryState(patient_id="P001", memory_id="M001")

    print("\nInitial State:")
    print(state.to_dict())

    # Stage 1: Recognition
    state.add_prompt("Do you recognize this person?")
    state.add_answer("Yes, that is my brother Ramesh.")
    state.add_recalled_information("person", "Ramesh")

    print("\nAfter Recognition:")
    print(state.to_dict())

    # Stage 2: Association
    state.next_stage()
    print("\nNext Stage:")
    print(state.stage, state.get_stage_name())

    state.add_prompt("Who is this person?")
    state.add_answer("He is my brother.")
    state.add_recalled_information("relationship", "brother")

    # Move through remaining stages: Context -> Event -> Story
    state.next_stage()
    state.next_stage()
    state.next_stage()

    print("\nAt final stage:")
    print(state.stage, state.get_stage_name(), "| completed:", state.is_completed())

    # One more call is what actually marks the session complete
    state.next_stage()

    print("\nAfter marking complete:")
    print(state.stage, state.get_stage_name(), "| completed:", state.is_completed())

    # Calling again should be a no-op, not raise or overshoot MAX_STAGE
    state.next_stage()
    print("\nCalling next_stage() again after completion (should be unchanged):")
    print(state.stage, "| completed:", state.is_completed())

    print("\nFinal State:")
    print(state.to_dict())

    # -------------------------------------------------------
    # Merge test: recalling the same category across two
    # "stages" should accumulate, not overwrite.
    # -------------------------------------------------------

    print("\n" + "=" * 50)
    print("MERGE TEST — recalling 'places' across two stages")
    print("=" * 50)

    merge_state = MemoryState(patient_id="P002", memory_id="M002")

    # Stage A: patient recalls one place
    merge_state.add_recalled_information("places", ["Shillong"])
    print("After stage A:", merge_state.recalled_information["places"])

    # Stage B: patient recalls another place — should ADD, not replace
    merge_state.add_recalled_information("places", ["Ward's Lake", "shillong"])
    print("After stage B:", merge_state.recalled_information["places"])
    print("(Expected: both places present, 'shillong' not duplicated)")

    print("\n" + "=" * 50)
    print("MERGE TEST — recalling 'people' across two stages")
    print("=" * 50)

    # Stage A: name recalled without relationship yet
    merge_state.add_recalled_information(
        "people", [{"name": "Ramesh", "relationship": ""}]
    )
    print("After stage A:", merge_state.recalled_information["people"])

    # Stage B: same person, relationship now recalled — should FILL IN,
    # not create a second "Ramesh" entry
    merge_state.add_recalled_information(
        "people", [{"name": "Ramesh", "relationship": "brother"}]
    )
    print("After stage B:", merge_state.recalled_information["people"])
    print("(Expected: one Ramesh entry, relationship filled in)")