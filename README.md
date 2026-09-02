# sih2026
👥 6-Person Team — Detailed Work Distribution
👤 PERSON 1 — Patient Mobile App & Accessibility

Main responsibility: Build the complete patient-facing Flutter application and make it extremely simple for a dementia patient to use.

Technologies
Flutter
Dart
SQLite/Hive
Firebase
GPS/location plugins
TTS/STT integration
Features
🏠 Patient Home
Large, simple buttons
Today's date/day
Weather
Current location
Medicine status
Quick SOS button
Voice assistance
📅 Daily Orientation

Implement:

Day
Date
Time
Weather
Current location
Simple orientation messages

Example:

Good Morning, Maa ❤️

Today is Wednesday
September 2, 2026
You are at Home

☀️ Weather: Sunny

💊 Medicine at 10:00 AM
🌐 Regional Language UI

Support the UI for:

Assamese
Khasi
Manipuri
Mizo
Hindi
English

Person 1 manages the mobile-side localization, while Person 3 handles AI language processing.

📴 Offline Mode

Implement local storage for:

Games
Family information
Memory Vault content
Medicine reminders
Basic orientation
Recently used content

When internet returns:

Local Data
    ↓
Sync Manager
    ↓
FastAPI
    ↓
PostgreSQL
♿ Accessibility

This is especially important.

Implement:

Large fonts
High-contrast UI
Large buttons
Minimal menus
Voice navigation
Simple animations
Confirmation before important actions
Person 1 deliverables
Flutter App
├── Home
├── Orientation
├── Profile
├── Offline System
├── Localization
├── Navigation
└── Accessibility
👤 PERSON 2 — Cognitive Games & Adaptive Game Engine

Main responsibility: Everything related to cognitive stimulation.

Technologies
Flutter/Dart for game UI
Python for analytics/ML
FastAPI APIs
PostgreSQL
Scikit-learn if ML is required
Features
🧠 Memory Recall Games

Build:

Photo Matching

👩     👨     👧
 ↓     ↓     ↓
Match identical photos

Sequence Game

🍎 → 🏠 → 🚗 → ?

Patient selects the next item.

Pattern Game

🔴 🔵 🔴 🔵 ?
🧩 Jigsaw & Puzzle

Implement:

Jigsaw
Simple puzzles
Image-based puzzles
Matching
Ordering

Difficulty levels:

Easy       → 4 pieces
Medium     → 9 pieces
Hard       → 16 pieces
🎵 Music/Sound Memory

Examples:

Sound A → Sound B → Sound C

Repeat the sequence

Could include:

Familiar songs
Household sounds
Nature sounds
Instrument sounds
🎮 Adaptive Games

This is important.

Track:

Accuracy
Response time
Attempts
Hints used
Mistakes
Completion rate

Then:

Performance
     ↓
Difficulty Engine
     ↓
Next difficulty

Example:

Patient performs very well
        ↓
Increase difficulty

Patient struggles
        ↓
Decrease difficulty
📊 Cognitive scoring

Person 2 sends game data to backend:

patient_id
game_id
score
accuracy
response_time
difficulty
timestamp

Person 6 later converts this into caregiver analytics.

Person 2 deliverables
Games
├── Memory Recall
├── Photo Matching
├── Sequence
├── Pattern
├── Jigsaw
├── Puzzle
├── Music Memory
└── Adaptive Difficulty
👤 PERSON 3 — AI, Voice & Memory Reconstruction

Main responsibility: This is the AI brain of the project.

Technologies
Python
LLM API
Speech-to-Text
Text-to-Speech
NLP
OpenAI/Gemini API
FastAPI
AI prompt engineering
🗣️ AI Voice Companion

Flow:

Patient speaks
      ↓
Speech-to-Text
      ↓
AI/LLM
      ↓
Context + Patient Memory
      ↓
Response
      ↓
Text-to-Speech
      ↓
Patient hears response

The companion should have a calm, simple conversational style.

🧠 Personal Memory Vault

This is one of your strongest features.

Patient/caregiver can create:

Memory:
"My Childhood"

Photo:
[Childhood photo]

People:
Father, Mother

Place:
Village

Event:
School days

Voice:
Patient's recorded story

Person 3 develops the AI processing that converts the memory into structured elements.

For example:

Voice Story
     ↓
Speech-to-Text
     ↓
NLP
     ↓
Extract:
People
Places
Events
Dates
Objects
Emotions/context
     ↓
Memory Graph
🧩 Memory Reconstruction Engine

This should be Person 3's flagship feature.

Suppose the memory is:

Family trip to Shillong.

The system stores:

SHILLONG TRIP
│
├── People
│   ├── Mother
│   ├── Father
│   └── Brother
│
├── Place
│   └── Shillong
│
├── Event
│   └── Family Trip
│
└── Photos

Then the AI generates progressive prompts.

Stage 1 — Recognition

"Do you recognize this person?"

Stage 2 — Association

"Who is this person?"

Stage 3 — Context

"Do you remember where you went with them?"

Stage 4 — Event

"What did you do there?"

Stage 5 — Story

"Can you tell me about that trip?"

The system uses previous answers to choose the next prompt.

Memory Elements
       ↓
Prompt Generator
       ↓
Patient Response
       ↓
Response Analysis
       ↓
Next Prompt
       ↓
Reconstructed Story
🌐 Regional-language AI

Person 3 handles:

Speech recognition
AI responses
Translation
TTS
Regional-language prompts

for supported languages.

🔊 Personalized Voice

Caregiver records:

"Mummy, please take your medicine."

Person 3 handles the audio processing/storage/playback integration, while Person 5 handles the backend storage/API.

Person 3 deliverables
AI
├── Voice Companion
├── Speech-to-Text
├── LLM
├── Text-to-Speech
├── Personal Memory Vault AI
├── Memory Reconstruction Engine
├── Regional Language AI
└── Personalized Voice
👤 PERSON 4 — Computer Vision, GPS & Emergency Safety

Main responsibility: Patient identification + physical safety.

Technologies
Python
OpenCV
InsightFace
Flutter location APIs
Google Maps
Firebase Cloud Messaging
Geofencing
👨‍👩‍👧 Face–Name Association

Caregiver adds:

Photo → Mother
Photo → Father
Photo → Brother

System creates face embeddings.

Family Photo
      ↓
Face Detection
      ↓
Face Embedding
      ↓
Store

Later:

Camera
 ↓
Face
 ↓
Embedding
 ↓
Compare
 ↓
Recognize
 ↓
"Mummy"

You can also connect the person's recorded voice:

Recognized:
Mother

        ↓

"Hi Maa, this is your daughter."
🏠 Safe Return Home

Person 4 handles:

GPS
Current location
Home location
Route calculation
Maps
Voice navigation
Geofencing

Example:

Patient leaves safe zone
          ↓
Geofence triggered
          ↓
Patient gets alert
          ↓
"You're outside your usual area."
          ↓
Voice navigation
          ↓
Home
📍 Live / Last Location

Track:

Current location
Last known location
Timestamp
Location history

Dashboard receives this information from Person 5's APIs.

🚨 Emergency SOS

Patient presses:

       🚨 SOS

Then:

SOS
 ↓
GPS Location
 ↓
FastAPI
 ↓
Firebase
 ↓
Caregiver

Caregiver sees:

🚨 EMERGENCY

Patient needs help.

Last location:
[Map]

Time:
10:42 AM
Person 4 deliverables
Safety
├── Face Recognition
├── Face–Name Association
├── GPS
├── Live Location
├── Last Location
├── Geofencing
├── Safe Return Home
└── Emergency SOS
👤 PERSON 5 — Backend, Database, Security & Integration

Main responsibility: The central infrastructure.

This person is basically the bridge between everyone.

Technologies
Python
FastAPI
PostgreSQL
SQLAlchemy
JWT/Firebase Auth
Firebase Cloud Messaging
Cloud Storage
REST APIs
🗄️ Database

Design tables for:

Users
Patients
Caregivers
Family Members
Memories
Memory Elements
Voice Recordings
Games
Game Results
Cognitive Scores
Medicines
Reminders
Reminder History
Locations
SOS Alerts
Activities
Sleep Data
Languages
🔌 APIs

Person 5 creates APIs such as:

POST   /auth/login

GET    /patients/{id}

POST   /games/result

GET    /games/performance

POST   /memories

GET    /memories/{id}

POST   /medicines

POST   /reminders

GET    /locations/{patient_id}

POST   /location

POST   /emergency/sos

GET    /analytics/{patient_id}
💊 Medicine & Routine System

Caregiver configures:

Medicine:
Donepezil

Time:
9:00 AM

Voice:
"Mummy, please take your medicine."

Backend schedules and records:

Scheduled
 ↓
Reminder sent
 ↓
Taken / Missed
 ↓
Database
 ↓
Dashboard
🔔 Notifications

Use Firebase Cloud Messaging for:

SOS
Missed medicine
Important alerts
Geofence alerts
Caregiver notifications
🔐 Security

Very important because you're handling sensitive personal information.

Person 5 handles:

Authentication
Authorization
Patient/caregiver roles
Secure API access
Encrypted transport
Access control
Secure storage policies
Person 5 deliverables
Backend
├── FastAPI
├── PostgreSQL
├── Authentication
├── APIs
├── Notifications
├── Storage
├── Sync
├── Security
└── Integration
👤 PERSON 6 — Caregiver Dashboard, Analytics & Remote Management

Main responsibility: Everything the caregiver sees and controls.

Technologies
React
TypeScript
Tailwind CSS
Recharts
Google Maps
REST APIs
📊 Main Dashboard

Example:

┌───────────────────────────────────────┐
│          CAREGIVER DASHBOARD          │
├───────────────────────────────────────┤
│ Patient: Maa                          │
│                                       │
│ 🧠 Cognitive Score       78            │
│ 💊 Medicine Adherence    92%           │
│ 🎮 Games Today           4             │
│ 📍 Status                At Home       │
│ 🚨 Emergency             None          │
└───────────────────────────────────────┘
🧠 Cognitive Analytics

Display:

Game performance
Accuracy
Response time
Difficulty progression
Cognitive trends
Activity frequency

Charts:

Cognitive Performance
       📈
  90 ┤       ╭──╮
  80 ┤   ╭───╯  ╰──
  70 ┤───╯
     └──────────────
       Days

Important: present these as activity/performance trends, not as a medical diagnosis.

💊 Medicine Dashboard

Show:

Medicine adherence: 92%

Taken       █████████ 92%
Missed      █ 8%

Also:

Today's medicines
Missed medicines
Reminder history
Adherence trends
📍 Location Dashboard

Show:

Current location
Last location
Location history
Safe zone
Route home

Using Google Maps.

🚨 Emergency Dashboard

When SOS occurs:

🚨 SOS ALERT

Patient: Maa

Time: 10:42 AM

Location:
[MAP]

[Call Caregiver]
[View Route]
[Mark Alert Resolved]
👨‍👩‍👧 Family / Face Management

Caregiver can:

Add family member
Upload photo
Add name
Add relationship
Add voice association
Edit/remove person
🧠 Memory Vault Management

Caregiver can help create memories:

+ Add Memory

Title:
"My First School"

📸 Photos
👥 People
📍 Place
📅 Date
🎙️ Voice Story

[Save Memory]

They can also see the patient's reconstructed stories and recall activity.

💊 Remote Reminder Configuration

Caregiver can remotely configure:

Medicine
Time
Frequency
Voice recording
Reminder type

Changes go:

Dashboard
   ↓
FastAPI
   ↓
Patient App
📈 Activity & Sleep

Dashboard can display:

Daily activity
Game time
App usage
Reminder responses
Sleep/activity data if your app/device has a reliable source for it
Person 6 deliverables
Caregiver Dashboard
├── Overview
├── Cognitive Analytics
├── Game Analytics
├── Medicine
├── Reminders
├── Memory Vault
├── Family Management
├── Location
├── SOS
├── Activity
└── Settings
🔗 How the 6 People Work Together

This is the most important part.

Nobody should build their module completely separately.

                         ┌───────────────┐
                         │   PERSON 6    │
                         │   CAREGIVER   │
                         │   DASHBOARD   │
                         └───────┬───────┘
                                 │
                                 ↓
┌──────────────┐        ┌────────────────┐        ┌──────────────┐
│   PERSON 1   │◄──────►│    PERSON 5    │◄──────►│   PERSON 3   │
│   FLUTTER    │        │    BACKEND     │        │     AI       │
│ PATIENT APP  │        │ FastAPI + DB   │        │ VOICE/MEMORY │
└──────┬───────┘        └────────┬───────┘        └──────────────┘
       │                          │
       ↓                          ↓
┌──────────────┐          ┌──────────────┐
│   PERSON 2   │          │   PERSON 4   │
│    GAMES     │          │ SAFETY/GPS   │
│  + ADAPTIVE  │          │ FACE + SOS   │
└──────────────┘          └──────────────┘
