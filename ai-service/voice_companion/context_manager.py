"""
Context Manager for the AI Voice Companion.

Stores recent conversation messages for each conversation_id.
This helps the LLM maintain context across multiple turns.

NOTE: This is in-memory storage only — all conversation history is
lost if the process restarts, and it will NOT be shared across
multiple server instances/workers. For production, Person 5's
backend/database should be the source of truth for conversation
history; this class is best used as a fast local cache layered
on top of that, not a replacement for it.
"""

import threading
from typing import Dict, List


class ContextManager:
    """Manage conversation history for voice companion sessions."""

    def __init__(self, max_messages: int = 10):
        """
        Args:
            max_messages: Maximum number of messages to keep
                          for each conversation. Must be positive.
        """
        if max_messages <= 0:
            raise ValueError("max_messages must be a positive integer.")

        self.max_messages = max_messages

        # Example:
        # {
        #     "C001": [
        #         {"role": "user", "content": "Hello"},
        #         {"role": "assistant", "content": "Hello! How are you?"}
        #     ]
        # }
        self.conversations: Dict[str, List[Dict[str, str]]] = {}
        self._lock = threading.Lock()

    # ---------------------------------------------------------
    # Create a conversation
    # ---------------------------------------------------------

    def create_conversation(self, conversation_id: str) -> None:
        """Create a new conversation if it does not already exist."""
        if not conversation_id:
            raise ValueError("conversation_id is required")

        with self._lock:
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []

    # ---------------------------------------------------------
    # Add a message
    # ---------------------------------------------------------

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ) -> None:
        """
        Add a message to a conversation.

        role should normally be:
            user
            assistant
        """
        if not conversation_id:
            raise ValueError("conversation_id is required")

        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")

        if role not in {"user", "assistant", "system"}:
            raise ValueError("role must be 'user', 'assistant', or 'system'")

        with self._lock:
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []

            self.conversations[conversation_id].append(
                {"role": role, "content": content.strip()}
            )

            # Keep only the most recent messages
            history = self.conversations[conversation_id]
            if len(history) > self.max_messages:
                self.conversations[conversation_id] = history[-self.max_messages:]

    # ---------------------------------------------------------
    # Get conversation history
    # ---------------------------------------------------------

    def get_history(self, conversation_id: str) -> List[Dict[str, str]]:
        """Return conversation history."""
        with self._lock:
            return self.conversations.get(conversation_id, []).copy()

    # ---------------------------------------------------------
    # Get recent context as text
    # ---------------------------------------------------------

    def get_context(self, conversation_id: str) -> str:
        """
        Convert conversation history into text that can
        be given to the LLM.
        """
        history = self.get_history(conversation_id)

        if not history:
            return ""

        context_lines = [
            f"{message['role'].capitalize()}: {message['content']}"
            for message in history
        ]

        return "\n".join(context_lines)

    # ---------------------------------------------------------
    # Clear conversation
    # ---------------------------------------------------------

    def clear_conversation(self, conversation_id: str) -> None:
        """Delete all messages from a conversation."""
        with self._lock:
            self.conversations.pop(conversation_id, None)

    # ---------------------------------------------------------
    # Check conversation
    # ---------------------------------------------------------

    def exists(self, conversation_id: str) -> bool:
        """Check whether a conversation exists."""
        with self._lock:
            return conversation_id in self.conversations

    # ---------------------------------------------------------
    # Number of messages
    # ---------------------------------------------------------

    def message_count(self, conversation_id: str) -> int:
        """Return number of stored messages."""
        with self._lock:
            return len(self.conversations.get(conversation_id, []))


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    context_manager = ContextManager(max_messages=10)

    conversation_id = "C001"

    context_manager.add_message(conversation_id, "user", "Hello, my name is Rina.")
    context_manager.add_message(
        conversation_id, "assistant", "Hello Rina! It is nice to talk with you."
    )
    context_manager.add_message(conversation_id, "user", "I like gardening.")

    print("Conversation history:")
    print(context_manager.get_history(conversation_id))

    print("\nLLM Context:")
    print(context_manager.get_context(conversation_id))