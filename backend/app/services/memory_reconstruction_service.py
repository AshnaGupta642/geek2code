class MemoryReconstructionService:

    def start_session(
        self,
        patient_id: int,
        memory_id: int,
        language: str
    ) -> dict:

        raise NotImplementedError(
            "Memory Reconstruction AI service is not connected yet."
        )

    def submit_answer(
        self,
        session_id: str,
        patient_id: int,
        memory_id: int,
        answer_text: str
    ) -> dict:

        raise NotImplementedError(
            "Memory Reconstruction AI service is not connected yet."
        )