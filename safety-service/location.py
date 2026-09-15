import httpx
from fastapi import APIRouter, Header, HTTPException

router = APIRouter(prefix="/location", tags=["Location"])

BACKEND_URL = "http://127.0.0.1:8000"


@router.post("/")
async def send_location(
    location_data: dict,
    authorization: str | None = Header(default=None)
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization token required"
        )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/location/",
                json=location_data,
                headers={
                    "Authorization": authorization
                }
            )

        return response.json()

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Backend unavailable: {str(e)}"
        )