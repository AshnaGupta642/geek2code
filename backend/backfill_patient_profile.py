"""
One-off backfill script.

Creates a Patient profile row for every existing User with role='patient'
that doesn't already have one. Needed because, before the auth.py fix,
registering a patient account never created a matching Patient row -
so /api/family and /api/memories 404 with "Patient profile not found"
for any account created before the fix.

Safe to run multiple times: it only inserts rows for users that are
still missing a Patient profile, so already-fixed accounts are skipped.

Usage (run from the backend/ folder, same place you'd run the FastAPI app):
    python backfill_patient_profiles.py
"""

from app.database.database import SessionLocal
from app.models.user import User
from app.models.patient import Patient


def backfill():
    db = SessionLocal()
    try:
        patient_users = db.query(User).filter(User.role == "patient").all()

        created = 0
        skipped = 0

        for user in patient_users:
            existing = (
                db.query(Patient)
                .filter(Patient.user_id == user.id)
                .first()
            )

            if existing:
                skipped += 1
                continue

            db.add(Patient(user_id=user.id))
            created += 1
            print(f"Creating Patient profile for user_id={user.id} ({user.email})")

        db.commit()

        print(f"\nDone. Created {created} patient profile(s), {skipped} already had one.")

    finally:
        db.close()


if __name__ == "__main__":
    backfill()