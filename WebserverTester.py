# WebserverTester.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

logger = None   # will be set by Main.py

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

program_start_time = datetime.now()

def set_logger(parking_logger):

    #Called by Main.py to give this module its logger.
    global logger
    logger = parking_logger


def get_program_uptime(start_time):
    current_time = datetime.now()
    uptime = current_time - start_time
    return f"{uptime.days}:{(uptime.seconds//3600)%24}:{(uptime.seconds//60)%60}:{uptime.seconds%60}"


@app.get("/uptime")
def uptime():
    return f"Meshtastic Parking Server Uptime: {get_program_uptime(program_start_time)}"


@app.get("/api")
def api():
    if logger is None:
        return {"error": "Logger not initialized"}

    status = logger.get_lot_status()

    return {
        "ParkingLotA": {
            "Free": status["Lot North"]["available"],
            "Occupied": status["Lot North"]["current"]
        },
        "ParkingLotB": {
            "Free": status["Lot East"]["available"],
            "Occupied": status["Lot East"]["current"]
        },
        "ParkingLotC": {
            "Free": status["Lot West"]["available"],
            "Occupied": status["Lot West"]["current"]
        },
    }
