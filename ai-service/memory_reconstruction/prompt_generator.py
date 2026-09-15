"""
Memory Reconstruction Prompt Generator

Generates simple, dementia-friendly recall prompts
based on the current reconstruction stage.
"""

from typing import Any, Dict, List

try:
    # Normal case: prompt_generator.py imported as part of the
    # memory_reconstruction package.
    from .memory_state import (
        RECOGNITION,
        ASSOCIATION,
        CONTEXT,
        EVENT,
        STORY,
        MemoryState,
    )
except ImportError:
    # Fallback for running this file directly (e.g. PyCharm's Run button),
    # where Python has no parent package to resolve the leading "."
    # against. Requires memory_state.py to be in the same folder.
    from memory_state import (
        RECOGNITION,
        ASSOCIATION,
        CONTEXT,
        EVENT,
        STORY,
        MemoryState,
    )


# A last-resort prompt used only if every candidate for a stage has
# already been shown to the patient (state.prompts). Kept generic and
# gentle on purpose — this should be rare in normal use.
FALLBACK_PROMPT = "Let's think about this together — is there anything else you remember?"


class PromptGenerator:
    """Generate progressive memory-recall questions."""

    def __init__(self) -> None:
        pass

    # ---------------------------------------------------------
    # Generate next prompt
    # ---------------------------------------------------------

    def generate_prompt(
        self,
        state: MemoryState,
        memory: Dict[str, Any],
    ) -> str:
        """
        Generate a prompt based on the current stage.

        If the "primary" prompt for this stage has already been shown
        to the patient (tracked in state.prompts), this falls back to
        the next unused option from generate_prompt_options() instead
        of repeating the same question verbatim — which matters if the
        caller asks again within the same stage (e.g. after an unclear
        answer, before advancing).

        Args:
            state:
                Current reconstruction session.

            memory:
                Structured memory / memory graph information.

        Returns:
            A short, patient-friendly question.
        """

        if state.is_completed():
            return "We have finished remembering this story together."

        if not isinstance(memory, dict):
            raise ValueError("memory must be a dictionary")

        candidate = self._primary_prompt(state.stage, memory)

        if candidate not in state.prompts:
            return candidate

        for option in self.generate_prompt_options(state, memory):
            if option not in state.prompts:
                return option

        # Every generated option has already been asked this session.
        return FALLBACK_PROMPT

    def _primary_prompt(self, stage: int, memory: Dict[str, Any]) -> str:
        """Route to the stage-specific prompt builder."""

        if stage == RECOGNITION:
            return self._recognition_prompt(memory)

        if stage == ASSOCIATION:
            return self._association_prompt(memory)

        if stage == CONTEXT:
            return self._context_prompt(memory)

        if stage == EVENT:
            return self._event_prompt(memory)

        if stage == STORY:
            return self._story_prompt(memory)

        return "Do you remember anything about this memory?"

    # ---------------------------------------------------------
    # Stage 1 — Recognition
    # ---------------------------------------------------------

    def _recognition_prompt(self, memory: Dict[str, Any]) -> str:
        """Ask the patient to recognize something."""

        people = memory.get("people", [])

        if people:
            person = people[0]

            if isinstance(person, dict):
                name = person.get("name", "")

                if name:
                    return f"Do you recognize {name}?"

        places = memory.get("places", [])

        if places:
            return f"Do you recognize {places[0]}?"

        return "Do you recognize anything from this memory?"

    # ---------------------------------------------------------
    # Stage 2 — Association
    # ---------------------------------------------------------

    def _association_prompt(self, memory: Dict[str, Any]) -> str:
        """Ask who or what something is connected to."""

        people = memory.get("people", [])

        if people:
            person = people[0]

            if isinstance(person, dict):
                name = person.get("name", "")
                relationship = person.get("relationship", "")

                if name and relationship:
                    return f"Who is {name} to you?"

                if name:
                    return f"Who is {name}?"

        places = memory.get("places", [])

        if places:
            return f"What do you remember about {places[0]}?"

        return "What does this memory remind you of?"

    # ---------------------------------------------------------
    # Stage 3 — Context
    # ---------------------------------------------------------

    def _context_prompt(self, memory: Dict[str, Any]) -> str:
        """Ask about the place, people, or situation."""

        places = memory.get("places", [])

        if places:
            place = places[0]
            return f"Do you remember being in {place}?"

        people = memory.get("people", [])

        if people:
            return "Who was with you at that time?"

        return "Do you remember where or when this happened?"

    # ---------------------------------------------------------
    # Stage 4 — Event
    # ---------------------------------------------------------

    def _event_prompt(self, memory: Dict[str, Any]) -> str:
        """Ask about what happened."""

        events = memory.get("events", [])

        if events:
            event = events[0]
            return f"Do you remember what happened during {event}?"

        return "What happened during this memory?"

    # ---------------------------------------------------------
    # Stage 5 — Story
    # ---------------------------------------------------------

    def _story_prompt(self, memory: Dict[str, Any]) -> str:
        """Ask the patient to tell the complete story."""

        return "Can you tell me what you remember about this?"

    # ---------------------------------------------------------
    # Generate multiple possible prompts
    # ---------------------------------------------------------

    def generate_prompt_options(
        self,
        state: MemoryState,
        memory: Dict[str, Any],
    ) -> List[str]:
        """
        Generate a small set of alternative prompts.

        Useful if one question has already been asked.
        """

        stage = state.stage

        if stage == RECOGNITION:
            options = [
                self._recognition_prompt(memory),
                "Does this look familiar to you?",
                "Do you remember this person or place?",
            ]

        elif stage == ASSOCIATION:
            options = [
                self._association_prompt(memory),
                "How do you know this person?",
                "What does this person or place mean to you?",
            ]

        elif stage == CONTEXT:
            options = [
                self._context_prompt(memory),
                "Do you remember where you were?",
                "Who was there with you?",
            ]

        elif stage == EVENT:
            options = [
                self._event_prompt(memory),
                "What did you do there?",
                "What happened next?",
            ]

        elif stage == STORY:
            options = [
                self._story_prompt(memory),
                "Would you like to tell me more about it?",
                "What is your favorite part of this memory?",
            ]

        else:
            options = ["What do you remember about this?"]

        # Remove duplicates while preserving order
        unique_options: List[str] = []

        for option in options:
            if option and option not in unique_options:
                unique_options.append(option)

        return unique_options


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":

    generator = PromptGenerator()

    memory = {
        "people": [{"name": "Ramesh", "relationship": "brother"}],
        "places": ["Shillong"],
        "events": ["the family trip"],
    }

    state = MemoryState(patient_id="P001", memory_id="M001")

    print("\nMemory Reconstruction Prompts")
    print("=" * 50)

    for stage in range(1, 6):
        state.stage = stage
        prompt = generator.generate_prompt(state, memory)
        print(f"\nStage {stage} ({state.get_stage_name()}):")
        print(prompt)

    print("\n" + "=" * 50)
    print("Repetition test (asking Recognition stage twice):")
    print("=" * 50)

    state.stage = RECOGNITION
    first = generator.generate_prompt(state, memory)
    state.add_prompt(first)
    print("1st ask:", first)

    second = generator.generate_prompt(state, memory)
    state.add_prompt(second)
    print("2nd ask (should differ):", second)

    print("\nPrompt Options:")
    print("-" * 50)

    state.stage = RECOGNITION
    options = generator.generate_prompt_options(state, memory)

    for option in options:
        print("-", option)