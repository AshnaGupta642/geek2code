import httpx
from fastapi import APIRouter, Header, HTTPException

router = APIRouter(prefix="/sos", tags=["Emergency"])

BACKEND_URL = "http://127.0.0.1:8000"


@router.post("/")
async def trigger_sos(
    emergency_data: dict,
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
                f"{BACKEND_URL}/api/emergency/sos",
                json=emergency_data,
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