class PersonalizedVoiceService:

    def process_voice(
        self,
        patient_id: int,
        caregiver_id: int,
        audio_url: str,
        reminder_type: str,
        reminder_text: str
    ) -> dict:

        raise NotImplementedError(
            "Personalized Voice AI service is not connected yet."
        )