from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database.database import engine
from app.database.base import Base

from app.models.user import User
from app.models.patient import Patient
from app.models.caregiver import Caregiver
from app.models.patient_caregiver import PatientCaregiver
from app.models.family_member import FamilyMember
from app.models.memory import Memory
from app.models.memory_element import MemoryElement
from app.models.memory_relationship import MemoryRelationship
from app.models.voice_recording import VoiceRecording
from app.models.memory_media import MemoryMedia

from app.api.auth import router as auth_router
from app.api.patients import router as patients_router, patient_router
from app.api.memories import router as memories_router

from app.api.medicines import router as medicines_router
from app.api.reminders import router as reminders_router
from app.api.reminder_history import router as reminder_history_router
from app.api.family import router as family_router
from app.api.caregiver import router as caregiver_router
from app.api.activity_events import router as activity_events_router
from app.api.alerts import router as alerts_router
from app.api import location
from app.api import safe_zones
from app.api import emergency
from app.api import sync
from app.api import games
from app.api import voice_recordings
from app.api.audio_upload import router as audio_upload_router
from app.api.device_tokens import router as device_token_router
from app.api.notifications import router as notifications_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Memora API",
    description="Backend API for Memora",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.mount(
    "/audio",
    StaticFiles(directory="uploads/audio"),
    name="audio"
)

app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(patient_router)
app.include_router(memories_router)
app.include_router(medicines_router)
app.include_router(reminder_history_router)
app.include_router(reminders_router)
app.include_router(family_router)
app.include_router(caregiver_router)
app.include_router(activity_events_router)
app.include_router(alerts_router)
app.include_router(location.router)
app.include_router(safe_zones.router)
app.include_router(emergency.router)
app.include_router(sync.router)
app.include_router(games.router)
app.include_router(voice_recordings.router)
app.include_router(audio_upload_router)
app.include_router(device_token_router)
app.include_router(notifications_router)


@app.get("/")
def home():
    return {
        "message": "Memora Backend is running!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

