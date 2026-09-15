from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from location import router as location_router
from geofence import router as geofence_router
from sos import router as sos_router


app = FastAPI(
    title="MindMate Safety Service",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(location_router)
app.include_router(geofence_router)
app.include_router(sos_router)


@app.get("/")
def root():
    return {
        "service": "MindMate Safety Service",
        "status": "running"
    }