class PersonalMemoryService:

    def process_memory(
        self,
        patient_id: int,
        memory_id: int,
        title: str,
        story_text: str | None,
        voice_recording_url: str | None,
        photo_urls: list[str]
    ) -> dict:

        # Person 3 will connect the actual
        # AI memory extraction pipeline here.

        raise NotImplementedError(
            "Personal Memory AI service is not connected yet."
        )