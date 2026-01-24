from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import audio, sensors
from services.udp_service import udp_service
from services.serial_service import serial_service
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SignSpeak Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up SignSpeak Backend...")
    try:
        udp_service.start()
        serial_service.start()
    except Exception as e:
        logger.error(f"Error during startup: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    udp_service.stop()
    # serial_service.stop()

# Routes
app.include_router(sensors.router)
app.include_router(audio.router, prefix="/audio", tags=["Audio"])

@app.get("/")
def root():
    return {"status": "SignSpeak backend running (WiFi/UDP Mode)"}
