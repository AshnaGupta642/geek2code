class MemoryGraphService:

    def generate_graph(
        self,
        memory_id: int,
        patient_id: int,
        people: list[str],
        places: list[str],
        events: list[str],
        photo_ids: list[str]
    ) -> dict:

        raise NotImplementedError(
            "Memory Graph AI service is not connected yet."
        )