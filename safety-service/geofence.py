from fastapi import APIRouter

router = APIRouter(prefix="/geofence", tags=["Geofence"])


@router.post("/status")
async def geofence_status(data: dict):

    inside = data.get("inside_safe_zone", False)

    if inside:
        return {
            "status": "SAFE",
            "message": "Patient is inside the safe zone."
        }

    return {
        "status": "OUTSIDE",
        "message": "Patient has left the safe zone."
    }