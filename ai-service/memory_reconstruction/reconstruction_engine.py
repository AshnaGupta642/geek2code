"""
Memory Reconstruction Engine

Orchestrates a full memory-reconstruction session by tying together:
- MemoryState        (tracks session progress)
- PromptGenerator    (generates the next recall question)
- ResponseAnalyzer   (analyzes what the patient recalled)
- StoryBuilder       (builds the final reconstructed story)

This is the entry point the rest of the app (e.g. conversation_manager.py)
should call — it should never need to touch memory_state.py,
prompt_generator.py, response_analyzer.py, or story_builder.py directly.
"""

import logging
from typing import Any, Dict, Optional

try:
    # Normal case: imported as part of the memory_reconstruction package.
    from .memory_state import MemoryState
    from .prompt_generator import PromptGenerator
    from .response_analyzer import ResponseAnalyzer
    from .story_builder import StoryBuilder
except ImportError:
    # Fallback for running this file directly (e.g. PyCharm's Run button),
    # where Python has no parent package to resolve the leading "."
    # against. Requires the other four files to be in the same folder.
    from memory_state import MemoryState
    from prompt_generator import PromptGenerator
    from response_analyzer import ResponseAnalyzer
    from story_builder import StoryBuilder

logger = logging.getLogger(__name__)

# If the patient can't recall anything for this many consecutive attempts
# on the same stage, the engine gently moves on rather than getting the
# patient stuck repeating the same question indefinitely.
MAX_ATTEMPTS_PER_STAGE = 3

REASSURANCE_MESSAGE = "That's okay. We don't have to remember everything right now."


class ReconstructionEngine:
    """
    Runs a complete memory-reconstruction session for one patient/memory,
    from the first recognition prompt through to the final story.
    """

    def __init__(
        self,
        prompt_generator: Optional[PromptGenerator] = None,
        response_analyzer: Optional[ResponseAnalyzer] = None,
        story_builder: Optional[StoryBuilder] = None,
        max_attempts_per_stage: int = MAX_ATTEMPTS_PER_STAGE,
    ) -> None:
        self.prompt_generator = prompt_generator or PromptGenerator()
        self.response_analyzer = response_analyzer or ResponseAnalyzer()
        self.story_builder = story_builder or StoryBuilder()
        self.max_attempts_per_stage = max_attempts_per_stage

        # Tracks consecutive non-recall attempts per stage, per session,
        # so a patient stuck on one stage doesn't loop forever. Keyed by
        # (patient_id, memory_id) so multiple concurrent sessions don't
        # interfere with each other.
        self._stage_attempts: Dict[Any, int] = {}

    # ---------------------------------------------------------
    # Start a new session
    # ---------------------------------------------------------

    def start_session(
        self,
        patient_id: str,
        memory_id: str,
        memory: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Start a new memory-reconstruction session.

        Args:
            patient_id: Unique patient identifier.
            memory_id: Identifier of the memory being reconstructed.
            memory: Structured memory (output of memory_extractor.py /
                memory_normalizer.py) that this session is built around.

        Returns:
            A session result dict — see _build_result() for shape.
        """
        if not isinstance(memory, dict):
            raise ValueError("memory must be a dictionary")

        state = MemoryState(patient_id=patient_id, memory_id=memory_id)
        self._stage_attempts[self._session_key(state)] = 0

        logger.info(
            "Started reconstruction session: patient=%s, memory=%s",
            patient_id,
            memory_id,
        )

        prompt = self.prompt_generator.generate_prompt(state, memory)
        state.add_prompt(prompt)

        return self._build_result(state, memory, acknowledgement=None, prompt=prompt)

    # ---------------------------------------------------------
    # Process a patient's answer
    # ---------------------------------------------------------

    def process_answer(
        self,
        state: MemoryState,
        answer: str,
        memory: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Process the patient's answer to the current prompt, update the
        session state, and decide the next step.

        Args:
            state: The session's current MemoryState (as returned/tracked
                since start_session()).
            answer: The patient's spoken/transcribed answer.
            memory: The same structured memory the session was started with.

        Returns:
            A session result dict — see _build_result() for shape.

        Raises:
            ValueError: If memory is not a dictionary.
        """
        if not isinstance(memory, dict):
            raise ValueError("memory must be a dictionary")

        if state.is_completed():
            # Nothing left to process; return the final story again
            # rather than re-analyzing an answer to a finished session.
            return self._build_result(
                state, memory, acknowledgement=None, prompt=None
            )

        state.add_answer(answer)
        analysis = self.response_analyzer.analyze_response(answer, memory)

        if analysis["recalled_information"]:
            for key, value in analysis["recalled_information"].items():
                state.add_recalled_information(key, value)

        session_key = self._session_key(state)
        acknowledgement: Optional[str] = None

        if analysis["needs_support"]:
            # Patient didn't recall anything and expressed uncertainty.
            # Reassure them and try again on the SAME stage, up to the
            # attempt limit, rather than immediately moving on.
            self._stage_attempts[session_key] = self._stage_attempts.get(session_key, 0) + 1
            acknowledgement = REASSURANCE_MESSAGE

            if self._stage_attempts[session_key] < self.max_attempts_per_stage:
                prompt = self.prompt_generator.generate_prompt(state, memory)
                state.add_prompt(prompt)
                return self._build_result(state, memory, acknowledgement, prompt)

            # Attempt limit reached on this stage — move on gently rather
            # than leaving the patient stuck on a question they can't answer.
            logger.info(
                "Max attempts reached on stage %s for patient=%s, memory=%s; advancing.",
                state.get_stage_name(),
                state.patient_id,
                state.memory_id,
            )

        # Either the patient recalled something meaningful, or we've hit
        # the attempt limit for this stage — advance to the next stage.
        self._stage_attempts[session_key] = 0
        state.next_stage()

        if state.is_completed():
            return self._build_result(state, memory, acknowledgement, prompt=None)

        prompt = self.prompt_generator.generate_prompt(state, memory)
        state.add_prompt(prompt)

        return self._build_result(state, memory, acknowledgement, prompt)

    # ---------------------------------------------------------
    # Build the result returned to the caller
    # ---------------------------------------------------------

    def _build_result(
        self,
        state: MemoryState,
        memory: Dict[str, Any],
        acknowledgement: Optional[str],
        prompt: Optional[str],
    ) -> Dict[str, Any]:
        """
        Build the standard result dict returned by start_session() and
        process_answer().

        Shape:
            {
                "patient_id": str,
                "memory_id": str,
                "stage": int,
                "stage_name": str,
                "completed": bool,
                "acknowledgement": str | None,   # reassurance text, if any
                "next_prompt": str | None,       # None only when completed
                "story": str | None,             # only populated when completed
                "recalled_information": dict,
            }
        """
        result: Dict[str, Any] = {
            "patient_id": state.patient_id,
            "memory_id": state.memory_id,
            "stage": state.stage,
            "stage_name": state.get_stage_name(),
            "completed": state.is_completed(),
            "acknowledgement": acknowledgement,
            "next_prompt": prompt,
            "story": None,
            "recalled_information": state.recalled_information,
        }

        if state.is_completed():
            result["story"] = self.story_builder.build_story(state, memory)
            logger.info(
                "Reconstruction session completed: patient=%s, memory=%s",
                state.patient_id,
                state.memory_id,
            )

        return result

    # ---------------------------------------------------------
    # Session key helper
    # ---------------------------------------------------------

    @staticmethod
    def _session_key(state: MemoryState) -> Any:
        """Build the per-session key used for stage-attempt tracking."""
        return (state.patient_id, state.memory_id)


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    engine = ReconstructionEngine()

    memory = {
        "people": [{"name": "Ramesh", "relationship": "brother"}],
        "places": ["Shillong", "Ward's Lake"],
        "events": ["a family trip"],
        "dates": ["Sunday"],
        "objects": ["blue school bag"],
        "emotions": ["happy"],
        "summary": "The patient lived in Shillong with their brother Ramesh.",
    }

    print("\n" + "=" * 60)
    print("SCENARIO 1 — Patient recalls everything smoothly")
    print("=" * 60)

    result = engine.start_session(patient_id="P001", memory_id="M001", memory=memory)
    state = MemoryState(patient_id="P001", memory_id="M001")
    # Re-fetch the real state object the engine used, since start_session
    # only returns a summary dict — rebuild it the way conversation_manager
    # would (kept here in-memory for the test instead of a session store).
    # For this test we reconstruct manually by re-running through the engine
    # with a state object we hold onto directly:

    state = MemoryState(patient_id="P001", memory_id="M001")
    prompt = engine.prompt_generator.generate_prompt(state, memory)
    state.add_prompt(prompt)
    print(f"\n[{state.get_stage_name()}] AI: {prompt}")

    answers = [
        "Yes, that is my brother Ramesh.",
        "We went to Shillong together.",
        "I remember being at Ward's Lake with him.",
        "We went there on Sunday and had a family trip.",
        "I carried my blue school bag and felt very happy.",
    ]

    for answer in answers:
        print(f"Patient: {answer}")
        result = engine.process_answer(state, answer, memory)

        if result["acknowledgement"]:
            print(f"AI: {result['acknowledgement']}")

        if result["completed"]:
            print("\n--- STORY ---")
            print(result["story"])
            break
        else:
            print(f"[{result['stage_name']}] AI: {result['next_prompt']}")

    print("\n" + "=" * 60)
    print("SCENARIO 2 — Patient can't recall, then attempt limit kicks in")
    print("=" * 60)

    state2 = MemoryState(patient_id="P002", memory_id="M001")
    prompt2 = engine.prompt_generator.generate_prompt(state2, memory)
    state2.add_prompt(prompt2)
    print(f"\n[{state2.get_stage_name()}] AI: {prompt2}")

    for i in range(4):
        answer = "I don't remember."
        print(f"Patient: {answer}")
        result2 = engine.process_answer(state2, answer, memory)

        if result2["acknowledgement"]:
            print(f"AI: {result2['acknowledgement']}")

        if result2["completed"]:
            print("\n--- STORY ---")
            print(result2["story"])
            break
        else:
            print(f"[{result2['stage_name']}] AI: {result2['next_prompt']}")