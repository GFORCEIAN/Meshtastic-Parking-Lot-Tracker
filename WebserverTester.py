# WebserverTester.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from starlette.responses import RedirectResponse

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


lotCounts:list = [(-1,-1,"Null"),(-1,-1,"Null"),(-1,-1,"Null")]

def set_logger(parking_logger):

    #Called by Main.py to give this module its logger.
    global logger
    logger = parking_logger

def setLots(lots:list):
    global lotCounts
    lotCounts= lots


def get_program_uptime(start_time):
    current_time = datetime.now()
    uptime = current_time - start_time
    return f"{uptime.days}:{(uptime.seconds//3600)%24}:{(uptime.seconds//60)%60}:{uptime.seconds%60}"

@app.get("/")
def Redirect():
    return RedirectResponse(url="/api")

@app.get("/uptime")
def uptime():
    return f"Meshtastic Parking Server Uptime: {get_program_uptime(program_start_time)}"


@app.get("/api")
def api():
    #if logger is None:
        #return {"error": "Logger not initialized"}
    #status = logger.get_lot_status()
    return {
        "Lot North": {
            "Free": lotCounts[0][0],
            "Occupied": lotCounts[0][1]
        },
        "Lot South": {
            "Free": lotCounts[1][0],
            "Occupied": lotCounts[1][1]
        },
        "Lot Far": {
            "Free": lotCounts[2][0],
            "Occupied": lotCounts[2][1]
        },
    }
