from app.database.database import SessionLocal
from app.models.game import Game


games = [
    {
        "game_id": "G001",
        "name": "Photo Matching",
        "game_type": "photo_matching",
        "difficulty": "easy",
        "description": "Match familiar people or objects with the correct pair.",
        "offline_supported": True
    },
    {
        "game_id": "G002",
        "name": "Memory Sequence",
        "game_type": "sequence",
        "difficulty": "easy",
        "description": "Remember and reproduce a sequence of items.",
        "offline_supported": True
    },
    {
        "game_id": "G003",
        "name": "Pattern Recognition",
        "game_type": "pattern",
        "difficulty": "easy",
        "description": "Identify and complete familiar visual patterns.",
        "offline_supported": True
    },
    {
        "game_id": "G004",
        "name": "Jigsaw Puzzle",
        "game_type": "jigsaw",
        "difficulty": "easy",
        "description": "Arrange pieces to complete a familiar picture.",
        "offline_supported": True
    },
    {
        "game_id": "G005",
        "name": "Music Memory",
        "game_type": "music_memory",
        "difficulty": "easy",
        "description": "Recognize familiar songs and sounds.",
        "offline_supported": True
    },
    {
        "game_id": "G006",
        "name": "Memory Recall",
        "game_type": "memory_recall",
        "difficulty": "easy",
        "description": "Recall information from the patient's personal memories.",
        "offline_supported": True
    }
]


def seed_games():

    db = SessionLocal()

    try:

        for game_data in games:

            existing_game = (
                db.query(Game)
                .filter(
                    Game.game_id == game_data["game_id"]
                )
                .first()
            )

            if existing_game:
                print(
                    f"{game_data['game_id']} already exists. Skipping."
                )
                continue

            game = Game(**game_data)

            db.add(game)

        db.commit()

        print("Games seeded successfully.")

    except Exception as e:

        db.rollback()
        print("Error:", e)

    finally:

        db.close()


if __name__ == "__main__":
    seed_games()