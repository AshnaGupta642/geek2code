from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.game import Game
from app.models.user import User

from app.schemas.game import (
    GameCreate,
    GameResponse
)

from app.core.dependencies import get_current_user
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.game import Game
from app.models.game_session import GameSession
from app.models.patient import Patient
from app.models.user import User
from app.schemas.game_session import GameStartRequest, GameStartResponse
from app.core.dependencies import get_current_user
from app.models.game_result import GameResult
from app.schemas.game_result import GameResultCreate, GameResultResponse
from datetime import datetime, timezone
from app.models.family_member import FamilyMember
from sqlalchemy import func
from app.models.game_result import GameResult
router = APIRouter(
    prefix="/api/games",
    tags=["Games"]
)


# --------------------------------------------------
# CREATE GAME
# --------------------------------------------------

@router.post(
    "/",
    response_model=GameResponse
)
def create_game(
    game_data: GameCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Only admin can create games
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can create games"
        )

    # Check duplicate game ID
    existing_game = (
        db.query(Game)
        .filter(Game.game_id == game_data.game_id)
        .first()
    )

    if existing_game:
        raise HTTPException(
            status_code=400,
            detail="Game ID already exists"
        )

    game = Game(
        game_id=game_data.game_id,
        name=game_data.name,
        game_type=game_data.game_type,
        difficulty=game_data.difficulty,
        description=game_data.description,
        offline_supported=game_data.offline_supported
    )

    db.add(game)
    db.commit()
    db.refresh(game)

    return game


# --------------------------------------------------
# GET ALL ACTIVE GAMES
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[GameResponse]
)
def get_games(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    games = (
        db.query(Game)
        .filter(Game.is_active == True)
        .order_by(Game.id)
        .all()
    )

    return games


# --------------------------------------------------
# GET GAME BY ID
# --------------------------------------------------

@router.get(
    "/{game_id}",
    response_model=GameResponse
)
def get_game(
    game_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    game = (
        db.query(Game)
        .filter(
            Game.game_id == game_id,
            Game.is_active == True
        )
        .first()
    )

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    return game

@router.post("/start", response_model=GameStartResponse)
def start_game(
    game_data: GameStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Find logged-in patient's profile
    patient = (
        db.query(Patient)
        .filter(Patient.user_id == current_user.id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    # 2. Find requested game
    game = (
        db.query(Game)
        .filter(
            Game.game_id == game_data.game_id,
            Game.is_active == True
        )
        .first()
    )

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    # 3. Generate unique session ID
    session_id = str(uuid.uuid4())

    # 4. Create game session
    session = GameSession(
        session_id=session_id,
        patient_id=patient.id,
        game_id=game.game_id,
        difficulty=game.difficulty,
        status="STARTED"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    # 5. Return game information to Patient App
    return {
        "session_id": session.session_id,
        "game_id": game.game_id,
        "difficulty": game.difficulty,
        "game_data": {
            "name": game.name,
            "game_type": game.game_type,
            "description": game.description
        },
        "started_at": session.started_at
    }
@router.post("/result", response_model=GameResultResponse)
def submit_game_result(
    result_data: GameResultCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Find logged-in patient
    patient = (
        db.query(Patient)
        .filter(Patient.user_id == current_user.id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    # 2. Find game session
    session = (
        db.query(GameSession)
        .filter(
            GameSession.session_id == result_data.session_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Game session not found"
        )

    # 3. Make sure this session belongs to this patient
    if session.patient_id != patient.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to submit this result"
        )

    # 4. Prevent submitting result twice
    if session.status == "COMPLETED":
        raise HTTPException(
            status_code=400,
            detail="Game session is already completed"
        )

    # 5. Calculate next difficulty
    if result_data.accuracy >= 80:
        next_difficulty = "medium"
    elif result_data.accuracy < 50:
        next_difficulty = "easy"
    else:
        next_difficulty = "easy"

    # 6. Save result
    result = GameResult(
        session_id=session.session_id,
        patient_id=patient.id,
        game_id=session.game_id,
        score=result_data.score,
        accuracy=result_data.accuracy,
        mistakes=result_data.mistakes,
        duration_seconds=result_data.duration_seconds,
        attempts=result_data.attempts,
        hints_used=result_data.hints_used,
        response_time=result_data.response_time,
        difficulty=session.difficulty,
        completed_at=result_data.completed_at
    )

    db.add(result)

    # 7. Mark session completed
    session.status = "COMPLETED"
    session.completed_at = result_data.completed_at

    db.commit()
    db.refresh(result)

    return {
        "success": True,
        "session_id": session.session_id,
        "game_id": session.game_id,
        "score": result.score,
        "accuracy": result.accuracy,
        "next_difficulty": next_difficulty
    }
@router.get("/performance/{patient_id}")
def get_game_performance(
    patient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Check that logged-in user is a caregiver
    if current_user.role != "caregiver":
        raise HTTPException(
            status_code=403,
            detail="Only caregivers can access game performance"
        )

    # 2. Check caregiver is linked to this patient
    from app.models.family_member import FamilyMember

    caregiver = (
        db.query(FamilyMember)
        .filter(
            FamilyMember.user_id == current_user.id,
            FamilyMember.patient_id == patient_id,
            FamilyMember.is_caregiver == True,
            FamilyMember.is_active == True
        )
        .first()
    )

    if not caregiver:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this patient's performance"
        )

    # 3. Get completed game results
    results = (
        db.query(GameResult)
        .filter(
            GameResult.patient_id == patient_id
        )
        .order_by(GameResult.completed_at.desc())
        .all()
    )

    # 4. Overall statistics
    games_completed = len(results)

    if games_completed > 0:
        average_score = round(
            sum(result.score for result in results) / games_completed,
            2
        )

        average_accuracy = round(
            sum(result.accuracy for result in results) / games_completed,
            2
        )
    else:
        average_score = 0
        average_accuracy = 0

    # 5. Per-game statistics
    performance_map = {}

    for result in results:

        if result.game_id not in performance_map:
            performance_map[result.game_id] = {
                "game_id": result.game_id,
                "games_played": 0,
                "total_score": 0,
                "total_accuracy": 0
            }

        performance_map[result.game_id]["games_played"] += 1
        performance_map[result.game_id]["total_score"] += result.score
        performance_map[result.game_id]["total_accuracy"] += result.accuracy

    performance = []

    for game in performance_map.values():

        games_played = game["games_played"]

        performance.append({
            "game_id": game["game_id"],
            "games_played": games_played,
            "average_score": round(
                game["total_score"] / games_played,
                2
            ),
            "average_accuracy": round(
                game["total_accuracy"] / games_played,
                2
            )
        })

    return {
        "patient_id": patient_id,
        "games_completed": games_completed,
        "average_score": average_score,
        "average_accuracy": average_accuracy,
        "performance": performance
    }
@router.get("/patient/{patient_id}")
def get_patient_games(
    patient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Find logged-in patient
    patient = (
        db.query(Patient)
        .filter(
            Patient.id == patient_id,
            Patient.user_id == current_user.id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this patient's games"
        )

    # 2. Get all active games
    games = (
        db.query(Game)
        .filter(Game.is_active == True)
        .order_by(Game.id)
        .all()
    )

    # 3. Return only fields needed by Patient App
    return {
        "games": [
            {
                "game_id": game.game_id,
                "name": game.name,
                "type": game.game_type,
                "difficulty": game.difficulty,
                "offline_supported": game.offline_supported
            }
            for game in games
        ]
    }
@router.get("/performance/{patient_id}/trend")
def get_cognitive_trend(
    patient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Check that logged-in user is a caregiver
    if current_user.role != "caregiver":
        raise HTTPException(
            status_code=403,
            detail="Only caregivers can access cognitive trends"
        )

    # 2. Check caregiver is linked to this patient
    caregiver = (
        db.query(FamilyMember)
        .filter(
            FamilyMember.user_id == current_user.id,
            FamilyMember.patient_id == patient_id,
            FamilyMember.is_caregiver == True,
            FamilyMember.is_active == True
        )
        .first()
    )

    if not caregiver:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this patient's trend"
        )

    # 3. Get completed game results
    results = (
        db.query(GameResult)
        .filter(
            GameResult.patient_id == patient_id
        )
        .order_by(GameResult.completed_at.asc())
        .all()
    )

    # 4. Not enough data
    if len(results) < 2:
        return {
            "patient_id": patient_id,
            "trend": "INSUFFICIENT_DATA",
            "message": "At least 2 completed games are required to calculate a trend.",
            "average_accuracy": (
                round(results[0].accuracy, 2)
                if results else 0
            ),
            "recent_accuracy": (
                round(results[-1].accuracy, 2)
                if results else 0
            ),
            "change_percentage": 0,
            "data_points": [
                {
                    "date": result.completed_at.isoformat(),
                    "accuracy": result.accuracy
                }
                for result in results
            ]
        }

    # 5. Calculate average accuracy
    average_accuracy = round(
        sum(result.accuracy for result in results)
        / len(results),
        2
    )

    # 6. Compare first and latest performance
    first_accuracy = results[0].accuracy
    recent_accuracy = results[-1].accuracy

    change_percentage = round(
        recent_accuracy - first_accuracy,
        2
    )

    # 7. Determine trend
    if change_percentage >= 10:
        trend = "IMPROVING"

    elif change_percentage <= -10:
        trend = "DECLINING"

    else:
        trend = "STABLE"

    # 8. Prepare graph data
    data_points = [
        {
            "date": result.completed_at.isoformat(),
            "accuracy": result.accuracy
        }
        for result in results
    ]

    return {
        "patient_id": patient_id,
        "trend": trend,
        "average_accuracy": average_accuracy,
        "recent_accuracy": recent_accuracy,
        "change_percentage": change_percentage,
        "data_points": data_points
    }