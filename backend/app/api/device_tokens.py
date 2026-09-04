from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.device_token import DeviceToken
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/api/device-tokens",
    tags=["Device Tokens"]
)


# --------------------------------
# Register / update device token
# --------------------------------
@router.post("/")
def register_device_token(
    token: str,
    platform: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if platform.lower() not in ["android", "ios", "web"]:
        raise HTTPException(
            status_code=400,
            detail="Platform must be android, ios, or web."
        )

    existing_token = (
        db.query(DeviceToken)
        .filter(DeviceToken.token == token)
        .first()
    )

    if existing_token:

        # Token already exists
        existing_token.user_id = current_user.id
        existing_token.platform = platform.lower()
        existing_token.is_active = True

        db.commit()
        db.refresh(existing_token)

        return {
            "message": "Device token updated successfully",
            "token_id": existing_token.id
        }

    # New token
    device_token = DeviceToken(
        user_id=current_user.id,
        token=token,
        platform=platform.lower(),
        is_active=True
    )

    db.add(device_token)
    db.commit()
    db.refresh(device_token)

    return {
        "message": "Device token registered successfully",
        "token_id": device_token.id
    }


# --------------------------------
# Get my device tokens
# --------------------------------
@router.get("/")
def get_my_device_tokens(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    tokens = (
        db.query(DeviceToken)
        .filter(
            DeviceToken.user_id == current_user.id,
            DeviceToken.is_active == True
        )
        .all()
    )

    return [
        {
            "id": token.id,
            "platform": token.platform,
            "is_active": token.is_active,
            "created_at": token.created_at,
            "updated_at": token.updated_at
        }
        for token in tokens
    ]


# --------------------------------
# Deactivate device token
# --------------------------------
@router.delete("/{token_id}")
def deactivate_device_token(
    token_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    device_token = (
        db.query(DeviceToken)
        .filter(
            DeviceToken.id == token_id,
            DeviceToken.user_id == current_user.id
        )
        .first()
    )

    if not device_token:
        raise HTTPException(
            status_code=404,
            detail="Device token not found."
        )

    device_token.is_active = False

    db.commit()

    return {
        "message": "Device token deactivated successfully"
    }