Wednesday 12:45 PM
Pasted markdown(4).md
File
AI-Based Cognitive Gaming & Personal Memory Assistance Platform for Elderly Dementia Patients in NER
👴 Patient-Side Features — Priority Order
🧠 Personal Memory Vault – Patients can record their life experiences, memories and stories through voice, with photos, people, places and events linked to each memory.
🧩 Memory Reconstruction Engine – Breaks personal memories into interconnected elements and uses progressive, voice-based recall prompts to help patients reconstruct and engage with their own life stories.
🎙️ Voice-First AI Companion – The entire patient-side platform can be operated primarily through natural voice commands instead of complicated menus or typing.
🎮 AI-Adaptive Cognitive Games – Automatically adapts game type and difficulty based on the patient's previous performance and engagement.
👨‍👩‍👧 Face–Name & Relationship Association – Uses family photos, names, relationships and familiar voices to create personalized recognition and recall activities.
🗣️ Multilingual & Regional Voice Support – Voice interaction in Assamese, Khasi, Manipuri, Mizo, Hindi and English, with culturally familiar content for NER users.
📅 Personalized Daily Orientation – Voice-based information about day, date, time, weather, location, upcoming activities and personalized routine.
💊 Medicine & Routine Reminders – Voice reminders for medicines, hydration, meals, appointments and daily activities.
❤️ Personalized Family Voice Reminders – Caregivers/family members can record reminders in their own voice, e.g., “Mummy, please take your medicine now.”
🧩 Personalized Memory Games & Puzzles – Photo matching, sequence recall, patterns, jigsaw puzzles, object recognition and activities generated using the patient's own memories.
🎵 Music & Sound Memory Activities – Uses familiar songs, sounds and patient-approved audio to create personalized memory and recognition activities.
🏠 Safe Return Home – GPS-based location assistance with simple voice-guided navigation when a patient has difficulty finding their way home.
🚨 Emergency SOS – Voice command or one-tap emergency alert to notify registered caregivers.
📍 Live / Last Location Sharing – Consent-based location sharing with caregivers and configurable safe-zone alerts.
📴 Offline-First Mode – Core games, saved memories, reminders and essential voice functions continue working without internet, with synchronization when connectivity returns.
👨‍👩‍👧 Caregiver Side — Priority Order
📊 AI-Powered Caregiver Dashboard – Central dashboard showing the patient's daily activity, cognitive-engagement trends, routines, reminders and alerts.
🧠 Cognitive Engagement Analytics – Tracks performance across different activities and identifies areas of stronger/weaker engagement over time without claiming medical diagnosis.
💊 Medicine & Routine Adherence – Shows completed/missed medicines, hydration and scheduled activities.
🎙️ Remote Voice & Reminder Management – Caregivers can remotely create reminders, upload family voices and configure patient routines.
🚨 Caregiver Alerts – Notifications for SOS, missed important routines, safe-zone exits and other configured events.
📍 Location Monitoring – Current/last known location and configurable safety-zone monitoring.
🔐 Personal Memory & Access Control – Caregivers can add, verify, categorize and control access to patient memories, photos and voice recordings. i am doing person 5 work how to start and tell me how to tell which person to connect with me and i will set up the repo and everything tell me how to begin i am the wall i have to connect everythingmake it easier for me pls
PERSON 3 — AI, Voice & Memory Reconstruction What I Need From Other Team Members Person Their Responsibility What I Need From Them Why I Need It Person 1 Flutter Patient App Patient audio, patient_id, selected language, patient answers, photos/audio uploaded by patient To process voice, communicate with the AI, and create/reconstruct memories Person 2 Cognitive Games Game type, score, accuracy, time taken, difficulty level, date/time Optional: AI can use performance as patient context and provide personalized encouragement Person 4 GPS, Safety, Face Recognition Current/last location, SOS status, recognized person's name/ID AI can respond appropriately when a patient is lost or connect recognized family members with memories Person 5 Backend + Database APIs, database storage, patient profile, memories, conversation history, audio/photo storage MOST IMPORTANT: My AI needs data from the database and needs a way to save its results Person 6 Caregiver Dashboard Family member information, caregiver-created memories, photos, memory descriptions, recorded stories/corrections Provides the personal memory data used by the Memory Vault and Reconstruction Engine Data Flow Feature Input I Receive Output I Return AI Voice Companion Patient audio, patient_id, language Transcript, AI response text, TTS audio Personal Memory Vault Voice story/text, photos, patient ID Extracted people, places, events, dates, emotions Memory Graph Structured memory elements Relationships between people, places, events and memories Memory Reconstruction Memory ID, patient answer, previous context Next personalized recall question, updated memory state Regional Language AI Audio/text + selected language Response in the patient's language Personalized Voice Caregiver voice recording + reminder information Processed audio ready for storage/playback My 3 Main Dependencies Priority Person Why 1 Person 5 Backend, database, APIs and storage 2 Person 1 Patient voice/audio and AI interaction 3 Person 6 Family and personal memory information Final note: Person 4 is needed for safety, GPS and face-recognition integration, while Person 2's game-performance data is optional for the initial AI module. is this you wanted or i should ask him more specifically
a8a5b12b-8086-426a-a443-477532f0b55a.pdf
PDF
person 2 and 4 ke liye bhi ye docs bana do
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6InBhdGllbnQiLCJleHAiOjE3ODgzNjQwMzZ9.HL0am9ezEgl_LYPoYfqNlxKnpNVT-qxEk1VrsllQSQk",
  "token_type": "bearer",
  "user_id": 1,
  "role": "patient"
}
👍
Pasted code(20260903-164930).py
Python

POST /api/reminders/event → Try it out i can't see this

👍
Pasted code(20260903-173548).py
Python
from datetime import datetime, timezone 
 
from sqlalchemy import ForeignKey, String, DateTime, Float, Integer 
from sqlalchemy.orm import Mapped, mapped_column 
 
from app.database.base import Base 
 
 
class GameResult(Base): 
    __tablename__ = "game_results" 
 
    id: Mapped[int] = mapped_column( 
        primary_key=True, 
        index=True 
    ) 
 
    session_id: Mapped[str] = mapped_column( 
        ForeignKey("game_sessions.session_id"), 
        nullable=False, 
        index=True 
    ) 
 
    patient_id: Mapped[int] = mapped_column( 
        ForeignKey("patients.id"), 
        nullable=False, 
        index=True 
    ) 
 
    game_id: Mapped[str] = mapped_column( 
        ForeignKey("games.game_id"), 
        nullable=False, 
        index=True 
    ) 
 
    score: Mapped[float] = mapped_column( 
        Float, 
        nullable=False 
    ) 
 
    accuracy: Mapped[float] = mapped_column( 
        Float, 
        nullable=False 
    ) 
 
    mistakes: Mapped[int] = mapped_column( 
        Integer, 
        default=0, 
        nullable=False 
    ) 
 
    duration_seconds: Mapped[int] = mapped_column( 
        Integer, 
        nullable=False 
    ) 
 
    attempts: Mapped[int] = mapped_column( 
        Integer, 
        default=1, 
        nullable=False 
    ) 
 
    hints_used: Mapped[int] = mapped_column( 
        Integer, 
        default=0, 
        nullable=False 
    ) 
 
    response_time: Mapped[float | None] = mapped_column( 
        Float, 
        nullable=True 
    ) 
 
    difficulty: Mapped[str] = mapped_column( 
        String(20), 
        nullable=False 
    ) 
 
    completed_at: Mapped[datetime] = mapped_column( 
        DateTime(timezone=True), 
        nullable=False 
    ) 
 
    created_at: Mapped[datetime] = mapped_column( 
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False 
    ) from datetime import datetime, timezone 
 
from sqlalchemy import ForeignKey, String, DateTime 
from sqlalchemy.orm import Mapped, mapped_column 
 
from app.database.base import Base 
 
 
class GameSession(Base): 
    __tablename__ = "game_sessions" 
 
    id: Mapped[int] = mapped_column( 
        primary_key=True, 
        index=True 
    ) 
 
    session_id: Mapped[str] = mapped_column( 
        String(100), 
        unique=True, 
        nullable=False, 
        index=True 
    ) 
 
    patient_id: Mapped[int] = mapped_column( 
        ForeignKey("patients.id"), 
        nullable=False, 
        index=True 
    ) 
 
    game_id: Mapped[str] = mapped_column( 
        ForeignKey("games.game_id"), 
        nullable=False, 
        index=True 
    ) 
 
    difficulty: Mapped[str] = mapped_column( 
        String(20), 
        nullable=False 
    ) 
 
    status: Mapped[str] = mapped_column( 
        String(20), 
        default="STARTED", 
        nullable=False 
    ) 
 
    started_at: Mapped[datetime] = mapped_column( 
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False 
    ) 
 
    completed_at: Mapped[datetime | None] = mapped_column( 
        DateTime(timezone=True), 
        nullable=True 
    )  
👍
i can't find it 
👍
Pasted code(20260903-180223).py
Python
POST /api/reminder-history/   ye nhi mill raha
👍
pakka ye mera kaam hai person1 ka nhi
👍

Haan, ye tumhara local backend URL hai:

http://127.0.0.1:8000

Toh tumhare liye Swagger:

http://127.0.0.1:8000/docs
⚠️ But team ko ye URL directly dene se kaam nahi karega

127.0.0.1 ka matlab "jis computer par request bheji ja rahi hai, wahi computer".

So agar Person 1 apne laptop se:

http://127.0.0.1:8000/api/memories/

hit karega, woh uske laptop ka backend dhoondhega, tumhara nahi.

Abhi development ke liye

Tum backend chala kar apne network ka IP use kar sakti ho:

http://YOUR_LOCAL_IP:8000

For example:

http://192.168.1.5:8000

Phir same Wi-Fi/network par connected team members use kar sakte hain.

Final integration ke liye

Best hai backend ko deploy karke ek common URL bana do:

https://memora-backend-xxxxx.com

Then everyone uses:

BASE_URL/api/...

and Swagger:

BASE_URL/docs

Abhi tum mujhe batao: kya tum sabko same Wi-Fi par connect karke integration karwaogi, ya backend ko internet par deploy karna hai? Uske according main exact next steps de dungi.

abhi mujhe batao mei ky kya karu jisse woh integration aasani se kar paaye
👍

Haan. Abhi tumhe unke integration ke liye backend side par ek proper handoff ready karna hai. Tumhara backend already working hai, so unnecessary code changes mat karo.

Abhi ye 6 kaam karo — isi order mein
1. Backend ko clean state mein rakho

Project structure roughly:

memora/
└── backend/
    ├── app/
    ├── uploads/
    ├── .env
    ├── requirements.txt
    └── ...

Ensure backend starts with:

uvicorn app.main:app --reload

and:

http://127.0.0.1:8000/docs

opens properly.

2. .gitignore check karo — VERY IMPORTANT

Backend GitHub par push karne se pehle:

.env
__pycache__/
*.pyc
.venv/
venv/
uploads/
firebase-service-account.json

.env kabhi GitHub par mat push karna.

3. requirements.txt updated rakho

Team member jab backend clone kare to:

pip install -r requirements.txt

se dependencies install ho jaani chahiye.

Tumhe unhe manually 10 packages ki list bhejne ki zarurat nahi honi chahiye.

4. Sabse important — API_CONTRACT.md banao

Backend repo ke root mein:

memora/
├── backend/
├── API_CONTRACT.md   ← NEW
├── README.md
└── ...

Is file mein har member ke liye:

Endpoint
Method
Authentication
Request body
Response
Purpose

likho.

Tumhare existing Swagger se ye information already available hai.

5. Team ko exact API mapping do

Ek simple document/message:

MEMORA BACKEND API HANDOFF

Base URL:
http://127.0.0.1:8000

Swagger:
http://127.0.0.1:8000/docs

Authentication:
Authorization: Bearer <JWT_TOKEN>

Then:

PERSON 1
Memory + Voice
→ /api/memories/
→ /api/voice-recordings/
→ /api/audio-upload/

PERSON 2
Games
→ /api/games/
→ /api/games/start
→ /api/games/result
→ /api/games/patient/{patient_id}

PERSON 3
AI/Cognitive
→ game performance
→ activity
→ memory data

PERSON 4
Safety
→ /api/location/
→ /api/safe-zones/
→ /api/emergency/sos

PERSON 6
Caregiver Dashboard
→ caregiver overview
→ activity
→ alerts
→ notifications
→ game performance
→ location
6. Unhe sample request + response bhi do

Ye integration ko bahut easy bana dega.

For example Person 2 ko:

POST /api/games/start

ka actual request aur actual response do.

Person 1 ko memory + audio ka example.

Person 4 ko location + SOS example.

Person 6 ko caregiver overview + notifications example.

Isse unhe Swagger mein baar-baar guess nahi karna padega.

⚠️ Ek problem abhi bhi hai: 127.0.0.1

Ye sirf tumhare laptop ke liye hai.

Agar team members alag laptops par hain, unko ye:

http://127.0.0.1:8000

mat dena.

Easiest temporary solution

Tum apna local IP nikaalo:

ipconfig

Usme IPv4 Address dekho.

Example:

192.168.1.7

Phir backend ko:

uvicorn app.main:app --host 0.0.0.0 --port 8000

se run karo.

Team same Wi-Fi par ho to woh use kar sakte hain:

http://192.168.1.7:8000/docs

Aur API base:

http://192.168.1.7:8000
Tumhare liye abhi exact checklist
☐ Backend starts without errors
☐ Swagger works
☐ requirements.txt updated
☐ .gitignore updated
☐ .env NOT pushed
☐ API_CONTRACT.md created
☐ Sample requests/responses documented
☐ GitHub push
☐ Local IP / deployed URL arrange
☐ Each member gets only the APIs they need
Aur ek important rule

Tum unke frontend/AI code mein integration mat karo.

Unka process:

Their Module
     ↓
Your API
     ↓
PostgreSQL

Agar Person 2 bole:

"Mujhe game result submit karne ke liye difficulty field bhi chahiye."

Tab woh requirement tumhe dega → tum backend API modify karogi.

Lekin tum uska game code connect nahi karogi.

Ab tumhara next best step API_CONTRACT.md banana hai. Main tumhare existing Memora backend ke saare endpoints ke according 
ready-to-copy API_CONTRACT.md ka complete content bana sakti hoon, member-wise, with request/response examples.

API_CONTRACT.md ye banao

👍

Done. Maine complete API_CONTRACT.md bana diya hai, member-wise APIs, authentication, sample requests, integration rules, reminders, notifications, sync, etc. ke saath.

Download API_CONTRACT.md

Isko apne Memora repo ke root mein rakh do:

memora/
├── backend/
├── patient-app/
├── caregiver-dashboard/
├── ai-service/
├── game-engine/
├── safety-service/
├── API_CONTRACT.md   ← ye
└── README.md

Ab team members ko ye file + Swagger URL dena enough hoga. 

API_CONTRACT.md
Document

Library
/
API_CONTRACT.md
MEMORA — API CONTRACT
1. Backend Information

Project: Memora
Backend: FastAPI
Database: PostgreSQL
Authentication: JWT Bearer Token

Local development
Base URL:
http://127.0.0.1:8000

Swagger:
http://127.0.0.1:8000/docs

127.0.0.1 works only when the backend is running on the same computer.
For team integration, use a shared/deployed backend URL or the host machine's local IP.

2. Authentication

Protected APIs require:

Authorization: Bearer <JWT_TOKEN>

Typical flow:

Register
   ↓
POST /api/auth/register
   ↓
Login
   ↓
POST /api/auth/login
   ↓
JWT token
   ↓
Use token in protected APIs

Do not commit JWT tokens or .env secrets to GitHub.

3. API Conventions
JSON is used for normal request/response bodies.
Audio upload uses multipart/form-data.
IDs are integers unless explicitly documented otherwise.
Game sessions use UUID-style session IDs.
Authentication and ownership are checked by the backend.
Do not connect directly to PostgreSQL from frontend/mobile applications.
Each module communicates through FastAPI APIs.
Swagger is the source of truth for the exact current request/response schema.
4. MEMBER 1 — Memories & Voice
Create Memory
POST /api/memories/

Auth: Patient

Example:

{
  "title": "My Wedding Day",
  "story_text": "A memory from my wedding day.",
  "summary": "Wedding day memory",
  "memory_type": "family",
  "tags": "wedding,family",
  "people": "Daughter,Husband",
  "event_date": "1995-05-20",
  "location": "Delhi",
  "cover_photo_url": "/images/wedding.jpg",
  "audio_url": null,
  "is_private": false
}

The backend controls is_approved; clients should not approve memories directly.

Get Memories
GET /api/memories/

Auth: Patient

Get One Memory
GET /api/memories/{memory_id}

Auth: Patient

Update Memory
PUT /api/memories/{memory_id}

Auth: Patient

Delete Memory
DELETE /api/memories/{memory_id}

Auth: Patient

Upload Audio
POST /api/audio-upload/

Auth: Patient
Content-Type: multipart/form-data

Supported formats:

MP3, WAV, M4A, OGG

Maximum file size: 10 MB.

The upload API stores the audio and creates the voice-recording information.

Create Voice Recording
POST /api/voice-recordings/

Auth: Patient

Example:

{
  "memory_id": 2,
  "family_member_id": 5,
  "audio_url": "/audio/wedding_memory.mp3",
  "language": "hi",
  "recording_type": "MEMORY_STORY",
  "duration_seconds": 45
}
Get Patient Voice Recordings
GET /api/voice-recordings/

Auth: Patient

Get One Voice Recording
GET /api/voice-recordings/{recording_id}

Auth: Patient

Caregiver Voice Recordings
GET /api/voice-recordings/caregiver/{patient_id}

Auth: Authorized caregiver

5. MEMBER 2 — Cognitive Games
Get Active Games
GET /api/games/
Get Game Details
GET /api/games/{game_id}
Start Game
POST /api/games/start

Auth: Patient

Example:

{
  "game_id": 1
}

The response contains a session_id. Store it and use it when submitting the game result.

Submit Game Result
POST /api/games/result

Auth: Patient

The result must reference the game session created by /api/games/start.

The backend:

validates session ownership
stores the result
completes the session
calculates the next difficulty using the current backend rule

Use Swagger for the exact current request schema.

Patient Game Data
GET /api/games/patient/{patient_id}
Caregiver Game Performance
GET /api/games/performance/{patient_id}

Auth: Caregiver

Game Performance Trend
GET /api/games/performance/{patient_id}/trend

Auth: Caregiver

6. MEMBER 3 — AI / Cognitive Analysis

The AI module should consume backend data through APIs instead of accessing PostgreSQL directly.

Useful endpoints:

GET /api/games/performance/{patient_id}
GET /api/games/performance/{patient_id}/trend
GET /api/caregiver/patients/{patient_id}/activity
GET /api/memories/
GET /api/memories/{memory_id}

If the AI module needs a new prediction/result endpoint, agree on the JSON contract with the backend developer before implementation.

Example conceptual result:

{
  "patient_id": 2,
  "prediction": "ATTENTION_REQUIRED",
  "confidence": 0.87
}

This is only an example contract. It is not an existing endpoint unless added to Swagger.

7. MEMBER 4 — Location & Safety
Send Patient Location
POST /api/location/

Auth: Patient

The backend associates the location with the authenticated patient.

Caregiver Latest Location
GET /api/location/caregiver/{patient_id}

Auth: Authorized caregiver

Caregiver Location History

Use the location-history endpoint currently shown in Swagger.

Auth: Authorized caregiver

Create Safe Zone
POST /api/safe-zones/
Get Safe Zones
GET /api/safe-zones/
Update Safe Zone
PUT /api/safe-zones/{safe_zone_id}
Delete Safe Zone
DELETE /api/safe-zones/{safe_zone_id}
SOS Emergency
POST /api/emergency/sos

Auth: Patient

When SOS is triggered:

an emergency event is stored
an SOS alert is created
caregiver in-app notification is generated

External push/SMS delivery is a separate notification integration.

8. MEMBER 6 — Caregiver Dashboard
Patient Overview
GET /api/caregiver/patients/{patient_id}/overview

Example response:

{
  "patient_id": 2,
  "name": "patient2",
  "age": 0,
  "language": "northeast",
  "orientation_status": "GOOD",
  "last_active": "2026-09-03T20:00:00+05:30",
  "overall_status": "ATTENTION",
  "alerts_count": 3,
  "medicine_adherence": 0,
  "missed_reminders": 4,
  "games_completed": 1,
  "average_game_accuracy": 85,
  "cognitive_trend": "INSUFFICIENT_DATA"
}

Use Swagger as the source of truth if fields change.

Patient Activity
GET /api/caregiver/patients/{patient_id}/activity

Provides caregiver-facing activity such as game completions, memory recall activity, voice-command activity, daily progress, and activity summary.

9. Alerts
Patient Alerts
GET /api/alerts/patient

Auth: Patient

Resolve Alert
PUT /api/alerts/{alert_id}/resolve
Caregiver Alerts
GET /api/alerts/caregiver/{patient_id}

Auth: Authorized caregiver

Automatic Missed Reminder Alert

When the backend detects at least 3 missed reminders in the configured 7-day period, it can create a MISSED_REMINDERS alert and a caregiver in-app notification.

Clients do not need to manually create this alert.

10. Notifications
Get Notifications
GET /api/notifications/

Auth: Current authenticated user

Get Unread Notifications
GET /api/notifications/unread
Get Unread Count
GET /api/notifications/unread-count
Mark Notification as Read
PUT /api/notifications/{notification_id}/read
Mark All as Read
PUT /api/notifications/read-all

Current notification types include:

SOS
SAFE_ZONE_EXIT
MISSED_REMINDERS

Notifications are currently stored as in-app database notifications. External FCM push delivery is a separate future integration.

11. Device Tokens
Register Device Token
POST /api/device-tokens/

Example:

{
  "token": "device-token-from-app",
  "platform": "android"
}

Supported platforms:

android
ios
web
Get Current User's Active Tokens
GET /api/device-tokens/
Deactivate Device Token
DELETE /api/device-tokens/{token_id}
12. Reminders
Create Reminder
POST /api/reminders/

Example:

{
  "medicine_id": 1,
  "voice_recording_id": 2,
  "reminder_type": "MEDICINE",
  "reminder_text": "Please take your medicine.",
  "scheduled_time": "14:30:00",
  "repeat_pattern": "DAILY"
}

A reminder can reference a voice recording.

Update Reminder
PUT /api/reminders/{reminder_id}
Get Reminders
GET /api/reminders/
Get One Reminder
GET /api/reminders/{reminder_id}
Delete Reminder
DELETE /api/reminders/{reminder_id}
Record Reminder Event
POST /api/reminders/event

Example:

{
  "reminder_id": 3,
  "status": "MISSED"
}
13. Offline Synchronization
Sync Offline Events
POST /api/sync/

Auth: Patient

Example:

{
  "patient_id": 2,
  "device_id": "test-device-001",
  "last_sync_at": "2026-09-04T09:01:03.380Z",
  "events": [
    {
      "event_id": "offline-test-001",
      "event_type": "REMINDER_MISSED",
      "data": {
        "reminder_id": 3,
        "status": "MISSED"
      },
      "timestamp": "2026-09-04T09:01:00+05:30"
    }
  ]
}

Response contains:

{
  "success": true,
  "synced_events": 1,
  "failed_events": [],
  "server_updates": {
    "reminders": [],
    "memories": [],
    "family": []
  },
  "next_sync_token": "server-generated-token"
}

The backend uses event_id + patient_id + device_id to prevent duplicate processing.

Server updates can contain current reminders, memories, and active family members.

14. Family Members

Useful endpoints:

POST /api/family-members/
GET  /api/family-members/
GET  /api/family-members/{family_member_id}
PUT  /api/family-members/{family_member_id}
DELETE /api/family-members/{family_member_id}

Use Swagger for the exact current schemas.

A family member can be marked as a caregiver.

15. Integration Rules
Rule 1 — Never access PostgreSQL directly

Correct:

Frontend / AI / Safety
        ↓
     FastAPI
        ↓
   PostgreSQL

Incorrect:

Frontend
   ↓
PostgreSQL
Rule 2 — Always use JWT
Authorization: Bearer <YOUR_TOKEN>
Rule 3 — Swagger is the source of truth

Local:

http://127.0.0.1:8000/docs

For team integration, replace the host with the shared/deployed backend URL.

Rule 4 — Backend handles ownership

Do not assume changing patient_id gives access to another patient. Backend authorization checks ownership and caregiver relationships.

Rule 5 — Each member integrates their own module
Member 1 → Memories/Voice → Backend
Member 2 → Games → Backend
Member 3 → AI → Backend
Member 4 → Safety → Backend
Member 6 → Caregiver Dashboard → Backend

The backend developer provides and maintains the API contract.

16. Quick API Map
Member	Main APIs
Member 1	Memories, Voice Recordings, Audio Upload
Member 2	Games, Game Sessions, Game Results
Member 3	Game Performance, Activity, Memory Data
Member 4	Location, Safe Zones, SOS
Member 5	Backend, Database, Authentication, APIs, Sync, Notifications
Member 6	Caregiver Overview, Activity, Alerts, Notifications, Performance, Location
17. Before Integration Checklist
Backend

Backend runs successfully

Swagger opens

requirements.txt is updated

.env is NOT committed

Secrets are NOT committed

API contract is shared

Shared/deployed base URL is provided

Other team members

Get the correct Base URL

Create/use their own test account

Obtain their own JWT

Add Authorization: Bearer <token>

Test the API in Swagger first

Connect their own module

Do not access PostgreSQL directly

Report missing API fields/endpoints to the backend developer

18. Current Limitations
Database/in-app notification functionality is available.
Actual Firebase/FCM push delivery can be added later.
Deployment can be completed after local integration is verified.
Final Integration Flow
                 MEMORA FASTAPI BACKEND
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ↓                 ↓                 ↓
   Patient App       AI Service      Caregiver Dashboard
       │                 │                 │
       ├─ Memories       ├─ Analysis       ├─ Overview
       ├─ Voice          ├─ Performance    ├─ Alerts
       ├─ Games          └─ Activity       ├─ Notifications
       ├─ Reminders                       ├─ Games
       ├─ Location                        └─ Location
       └─ SOS
                         │
                         ↓
                    PostgreSQL

Swagger is the final source of truth for exact schemas and endpoint details.