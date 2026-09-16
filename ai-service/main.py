"""
AI Engine — main.py

FastAPI entrypoint for the ai-service. This is called by the backend's
5 AI service stub classes (see backend/app/services/*.py) over HTTP —
ai-service and backend are separate processes/deployments.

Run locally:
    uvicorn main:app --reload --port 8001
(port 8001, not 8000, since the backend already uses 8000)
"""

import logging
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from voice_companion.conversation_manager import ConversationManager
from memory_vault.memory_extractor import MemoryExtractor
from memory_vault.memory_normalizer import MemoryNormalizer
from memory_vault.entity_extractor import EntityExtractor
from memory_graph.graph_builder import GraphBuilder
from memory_reconstruction.reconstruction_engine import ReconstructionEngine
from personalized_voice.voice_profile import VoiceProfile
from personalized_voice.voice_dataset import VoiceDatasetManager, VoiceRecording
from personalized_voice.voice_service import PersonalizedVoiceService as ElevenLabsVoiceService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Engine", version="0.1.0")
from fastapi.staticfiles import StaticFiles

app.mount("/audio", StaticFiles(directory="data/audio_responses"), name="audio")
# ---------------------------------------------------------
# Shared component instances
# ---------------------------------------------------------
conversation_manager = ConversationManager()
memory_extractor = MemoryExtractor()
memory_normalizer = MemoryNormalizer()
entity_extractor = EntityExtractor()
graph_builder = GraphBuilder()
reconstruction_engine = ReconstructionEngine()

# ---------------------------------------------------------
# In-memory stores.
#
# NOT PRODUCTION-SAFE: lost on restart, not shared across multiple
# workers. Same limitation context_manager.py already documents for
# conversation history. A real deployment should back these with a
# database or cache (Redis) shared across instances.
# ---------------------------------------------------------
_reconstruction_sessions: Dict[str, Dict[str, Any]] = {}
_caregiver_voice_profiles: Dict[int, tuple] = {}  # caregiver_id -> (VoiceProfile, ElevenLabsVoiceService)


# ---------------------------------------------------------
# Request models — one per backend service method
# ---------------------------------------------------------

class AIVoiceRequest(BaseModel):
    patient_id: int
    audio_url: Optional[str] = None
    audio_path: Optional[str] = None
    language: str
    conversation_id: str

class PersonalMemoryRequest(BaseModel):
    patient_id: int
    memory_id: int
    title: str
    story_text: Optional[str] = None
    voice_recording_url: Optional[str] = None
    photo_urls: List[str] = []


class MemoryGraphRequest(BaseModel):
    memory_id: int
    patient_id: int
    people: List[str] = []
    places: List[str] = []
    events: List[str] = []
    photo_ids: List[str] = []


class ReconstructionStartRequest(BaseModel):
    patient_id: int
    memory_id: int
    language: str
    story_text: str  # backend router must fetch this from Memory.story_text — see note below


class ReconstructionAnswerRequest(BaseModel):
    session_id: str
    patient_id: int
    memory_id: int
    answer_text: str


class PersonalizedVoiceRequest(BaseModel):
    patient_id: int
    caregiver_id: int
    audio_url: str
    reminder_type: str
    reminder_text: str


# ---------------------------------------------------------
# 1. AI Voice — maps to AIVoiceService.process_voice()
# ---------------------------------------------------------

@app.post("/ai-voice/process")
def ai_voice_process(request: AIVoiceRequest):
    try:
        return conversation_manager.process_conversation(
            patient_id=str(request.patient_id),
            audio_url=request.audio_url,
            audio_path=request.audio_path,
            language=request.language,
            conversation_id=request.conversation_id,

        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


# ---------------------------------------------------------
# 2. Personal Memory Vault — maps to PersonalMemoryService.process_memory()
# ---------------------------------------------------------

@app.post("/personal-memory/process")
def personal_memory_process(request: PersonalMemoryRequest):
    story_text = request.story_text

    if not story_text:
        if not request.voice_recording_url:
            raise HTTPException(
                status_code=400,
                detail="Either story_text or voice_recording_url is required.",
            )
        # A voice-only memory: transcribe it first.
        # TODO: needs a real STT call using request.voice_recording_url
        # (download + speech_to_text.py, same pattern as
        # conversation_manager._download_audio). Not wired up yet.
        raise HTTPException(
            status_code=501,
            detail="Voice-only memory ingestion (no story_text) is not implemented yet.",
        )

    try:
        raw_memory = memory_extractor.extract_memory(story_text)
        normalized = memory_normalizer.normalize_memory(raw_memory)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    return normalized  # {people, places, events, dates, objects, emotions, summary}


# ---------------------------------------------------------
# 3. Memory Graph — maps to MemoryGraphService.generate_graph()
# ---------------------------------------------------------

@app.post("/memory-graph/generate")
def memory_graph_generate(request: MemoryGraphRequest):
    """
    The backend's request only gives flat name lists (no relationships
    for people, since that's not tracked at this layer) — adapt into
    entity_extractor.py's expected shape before building the graph.
    """
    memory_like = {
        "people": [{"name": name, "relationship": ""} for name in request.people],
        "places": request.places,
        "events": request.events,
        "dates": [],
        "objects": [],
        "emotions": [],
    }

    try:
        entities = entity_extractor.extract_entities(memory_like)
        graph = graph_builder.build_graph(entities["entities"])
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return graph  # {nodes, relationships}


# ---------------------------------------------------------
# 4/5. Memory Reconstruction — maps to
# MemoryReconstructionService.start_session() / submit_answer()
# ---------------------------------------------------------

# @app.post("/memory-reconstruction/start")
# def reconstruction_start(request: ReconstructionStartRequest):
#     try:
#         raw_memory = memory_extractor.extract_memory(request.story_text)
#         memory = memory_normalizer.normalize_memory(raw_memory)
#     except (ValueError, RuntimeError) as exc:
#         raise HTTPException(status_code=502, detail=str(exc))

#     state = reconstruction_engine.start_session(
#         patient_id=str(request.patient_id), memory_id=str(request.memory_id), memory=memory
#     )
#     session_id = str(uuid.uuid4())
#     _reconstruction_sessions[session_id] = {"state": state, "memory": memory}

#     # question = reconstruction_engine.next_prompt(state, memory)
#     question = reconstruction_engine.prompt_generator.generate_prompt(state, memory)

#     return {
#         "session_id": session_id,
#         "current_stage": state.get_stage_name(),
#         "question": question,
#     }


# @app.post("/memory-reconstruction/answer")
# def reconstruction_answer(request: ReconstructionAnswerRequest):
#     session = _reconstruction_sessions.get(request.session_id)
#     if session is None:
#         raise HTTPException(status_code=404, detail="Unknown or expired session_id.")

#     state = session["state"]
#     memory = session["memory"]

#     analysis = reconstruction_engine.submit_answer(state, request.answer_text, memory)

#     if state.is_completed():
#         story = reconstruction_engine.build_final_story(state, memory)
#         del _reconstruction_sessions[request.session_id]
#         return {
#             "session_id": request.session_id,
#             "answer_analysis": {
#                 "recognized": analysis["recall_detected"],
#                 "confidence": analysis["confidence"],
#                 "extracted_information": analysis["matched_memory"],
#             },
#             "next_stage": "completed",
#             "next_question": story,
#             "updated_context": state.get_stage_name(),
#         }

#     next_question = reconstruction_engine.next_prompt(state, memory)
#     return {
#         "session_id": request.session_id,
#         "answer_analysis": {
#             "recognized": analysis["recall_detected"],
#             "confidence": analysis["confidence"],
#             "extracted_information": analysis["matched_memory"],
#         },
#         "next_stage": state.get_stage_name(),
#         "next_question": next_question,
#         "updated_context": state.get_stage_name(),
#     }

@app.post("/memory-reconstruction/start")
def reconstruction_start(request: ReconstructionStartRequest):
    try:
        raw_memory = memory_extractor.extract_memory(request.story_text)
        memory = memory_normalizer.normalize_memory(raw_memory)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    result = reconstruction_engine.start_session(
        patient_id=str(request.patient_id),
        memory_id=str(request.memory_id),
        memory=memory,
    )
    state = result["_state_object"]
    session_id = str(uuid.uuid4())
    _reconstruction_sessions[session_id] = {"state": state, "memory": memory}

    return {
        "session_id": session_id,
        "current_stage": result["stage_name"],
        "question": result["next_prompt"],
    }


@app.post("/memory-reconstruction/answer")
def reconstruction_answer(request: ReconstructionAnswerRequest):
    session = _reconstruction_sessions.get(request.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Unknown or expired session_id.")

    state = session["state"]
    memory = session["memory"]

    result = reconstruction_engine.process_answer(state, request.answer_text, memory)

    if result["completed"]:
        del _reconstruction_sessions[request.session_id]
        return {
            "session_id": request.session_id,
            "acknowledgement": result["acknowledgement"],
            "next_stage": "completed",
            "next_question": result["story"],
            "updated_context": result["stage_name"],
        }

    return {
        "session_id": request.session_id,
        "acknowledgement": result["acknowledgement"],
        "next_stage": result["stage_name"],
        "next_question": result["next_prompt"],
        "updated_context": result["stage_name"],
    }
# ---------------------------------------------------------
# 6. Personalized Voice — maps to PersonalizedVoiceService.process_voice()
# ---------------------------------------------------------

@app.post("/personalized-voice/process")
def personalized_voice_process(request: PersonalizedVoiceRequest):
    """
    First call for a given caregiver_id clones their voice from
    audio_url; later calls reuse the cached clone. This cache is
    in-memory only (see module note) — a real deployment should
    persist external_voice_id per caregiver in the backend's DB
    instead of re-cloning after every restart.
    """
    cached = _caregiver_voice_profiles.get(request.caregiver_id)

    if cached is None:
        profile = VoiceProfile(
            voice_id=f"caregiver_{request.caregiver_id}",
            name=f"Caregiver {request.caregiver_id}",
            language="en",
            is_personalized=True,
            is_available=True,
        )
        dataset = VoiceDatasetManager(voice_id=profile.voice_id)
        # NOTE: audio_url needs downloading first if it's remote — reusing
        # conversation_manager's download pattern. Assumed local path here.
        dataset.add_recording(
            VoiceRecording(
                recording_id="initial",
                file_path=request.audio_url,
                duration_seconds=60.0,  # placeholder — should come from real audio
                language="en",
            )
        )
        service = ElevenLabsVoiceService(voice_profile=profile, dataset=dataset)

        try:
            service.clone_voice(description=f"Caregiver {request.caregiver_id} voice")
        except RuntimeError as exc:
            raise HTTPException(status_code=502, detail=str(exc))

        _caregiver_voice_profiles[request.caregiver_id] = (profile, service)
    else:
        profile, service = cached

    try:
        output_path = service.generate_speech(text=request.reminder_text)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    return {
        "patient_id": request.patient_id,
        "caregiver_id": request.caregiver_id,
        "reminder_type": request.reminder_type,
        "audio_path": output_path,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)