"""
Common Schemas

Shared data structures used across multiple modules — NOT specific to
one feature area the way memory_vault/schemas.py (Person, MemoryEntity,
StructuredMemory) is specific to memory extraction.

Covers data Person 3 (this codebase) RECEIVES from other team members,
per the original team dependency doc:
    - Person 2 (Cognitive Games): game performance data
    - Person 5 (Backend): patient profile
    - Caregiver-provided medicine/routine reminders (surfaced via
      Person 5's backend or Person 6's caregiver dashboard)

These schemas exist so that data from these sources has one agreed
shape, and so conversation_manager.py's `extra_context` parameter has
something concrete to be filled with instead of staying an empty
string forever.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------
# Game Performance (from Person 2 — Cognitive Games)
# ---------------------------------------------------------

@dataclass
class GamePerformance:
    """
    One cognitive game session's results, as described in the team
    dependency doc: "Game type, score, accuracy, time taken, difficulty
    level, date/time."
    """

    game_type: str
    score: float
    accuracy: float  # expected as a percentage, 0-100
    time_taken_seconds: float
    difficulty_level: str
    played_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        self.game_type = self.game_type.strip()
        self.difficulty_level = self.difficulty_level.strip()
        if not self.game_type:
            raise ValueError("GamePerformance.game_type cannot be empty.")
        if self.accuracy < 0 or self.accuracy > 100:
            raise ValueError("GamePerformance.accuracy must be between 0 and 100.")
        if self.score < 0:
            raise ValueError("GamePerformance.score cannot be negative.")
        if self.time_taken_seconds < 0:
            raise ValueError("GamePerformance.time_taken_seconds cannot be negative.")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GamePerformance":
        """Build from a raw dict, e.g. from Person 2's/Person 5's API."""
        played_at_raw = data.get("played_at") or data.get("date_time")
        played_at = None
        if played_at_raw:
            try:
                played_at = datetime.fromisoformat(str(played_at_raw))
            except ValueError:
                played_at = None

        return cls(
            game_type=str(data.get("game_type", "")),
            score=float(data.get("score", 0)),
            accuracy=float(data.get("accuracy", 0)),
            time_taken_seconds=float(data.get("time_taken_seconds", data.get("time_taken", 0))),
            difficulty_level=str(data.get("difficulty_level", "")),
            played_at=played_at,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "game_type": self.game_type,
            "score": self.score,
            "accuracy": self.accuracy,
            "time_taken_seconds": self.time_taken_seconds,
            "difficulty_level": self.difficulty_level,
            "played_at": self.played_at.isoformat() if self.played_at else None,
        }

    def to_context_text(self) -> str:
        """
        Human-readable summary suitable for injecting into
        conversation_manager.py's `extra_context`, so the LLM can
        reference it (e.g. for personalized encouragement) — per the
        dependency doc: "AI can use performance as patient context and
        provide personalized encouragement."
        """
        when = f" on {self.played_at.strftime('%B %d')}" if self.played_at else ""
        return (
            f"The patient recently played a {self.difficulty_level} difficulty "
            f"'{self.game_type}' game{when}, scoring {self.score:.0f} points "
            f"with {self.accuracy:.0f}% accuracy in {self.time_taken_seconds:.0f} seconds."
        )


# ---------------------------------------------------------
# Medicine Reminder (from caregiver / backend)
# ---------------------------------------------------------

@dataclass
class MedicineReminder:
    """
    A single medicine reminder, as configured by a caregiver.

    IMPORTANT: this schema exists specifically so the LLM has REAL
    medicine information to reference, per prompts.py's
    ROUTINE_REMINDER_PROMPT instruction: "Do not invent medicine names,
    doses, or medical instructions. Use only information provided by
    the caregiver or backend." Before this schema existed, that
    instruction had nothing concrete to point to.
    """

    medicine_name: str
    dosage: str
    times: List[str] = field(default_factory=list)  # e.g. ["08:00", "20:00"]
    instructions: str = ""

    def __post_init__(self) -> None:
        self.medicine_name = self.medicine_name.strip()
        self.dosage = self.dosage.strip()
        self.instructions = self.instructions.strip()
        self.times = [t.strip() for t in self.times if t.strip()]
        if not self.medicine_name:
            raise ValueError("MedicineReminder.medicine_name cannot be empty.")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MedicineReminder":
        """Build from a raw dict, e.g. from the caregiver dashboard/backend."""
        return cls(
            medicine_name=str(data.get("medicine_name", "")),
            dosage=str(data.get("dosage", "")),
            times=[str(t) for t in data.get("times", [])],
            instructions=str(data.get("instructions", "")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "medicine_name": self.medicine_name,
            "dosage": self.dosage,
            "times": self.times,
            "instructions": self.instructions,
        }

    def to_context_text(self) -> str:
        """Human-readable summary for conversation_manager.py's `extra_context`."""
        times_str = ", ".join(self.times) if self.times else "an unspecified time"
        text = f"{self.medicine_name} ({self.dosage}) is scheduled at {times_str}."
        if self.instructions:
            text += f" Instructions: {self.instructions}"
        return text


def medicine_reminders_to_context_text(reminders: List[MedicineReminder]) -> str:
    """Combine multiple reminders into one context block."""
    if not reminders:
        return ""
    lines = [reminder.to_context_text() for reminder in reminders]
    return "The patient's medicine schedule:\n" + "\n".join(f"- {line}" for line in lines)


# ---------------------------------------------------------
# Patient Profile (from Person 5 — Backend)
# ---------------------------------------------------------

@dataclass
class PatientProfile:
    """
    Basic patient information, as would come from Person 5's backend.
    Kept intentionally minimal — this is NOT a medical record, just
    enough to personalize the conversation appropriately.
    """

    patient_id: str
    name: str = ""
    preferred_language: str = "en"

    def __post_init__(self) -> None:
        self.patient_id = self.patient_id.strip()
        self.name = self.name.strip()
        self.preferred_language = self.preferred_language.strip()
        if not self.patient_id:
            raise ValueError("PatientProfile.patient_id cannot be empty.")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PatientProfile":
        return cls(
            patient_id=str(data.get("patient_id", "")),
            name=str(data.get("name", "")),
            preferred_language=str(data.get("preferred_language", "en")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "preferred_language": self.preferred_language,
        }


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    game = GamePerformance.from_dict(
        {
            "game_type": "Memory Match",
            "score": 85,
            "accuracy": 92.5,
            "time_taken_seconds": 120,
            "difficulty_level": "medium",
            "played_at": "2026-09-08T10:00:00",
        }
    )
    print("Game performance:")
    print(game.to_dict())
    print(game.to_context_text())

    print("\nMedicine reminders:")
    reminders = [
        MedicineReminder(
            medicine_name="Donepezil",
            dosage="5mg",
            times=["08:00", "20:00"],
            instructions="Take with food.",
        ),
        MedicineReminder(medicine_name="Vitamin D", dosage="1 tablet", times=["09:00"]),
    ]
    print(medicine_reminders_to_context_text(reminders))

    print("\nPatient profile:")
    profile = PatientProfile.from_dict(
        {"patient_id": "P001", "name": "Rina", "preferred_language": "hi"}
    )
    print(profile.to_dict())