import os
import random

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import random

import uvicorn
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (your React dev server)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

program_start_time = datetime.now()

def get_program_uptime(start_time: datetime):
    current_time = datetime.now()
    uptime = current_time - start_time
    return f"{uptime.days}:{int((uptime.seconds/3600)%24)}:{int((uptime.seconds/60)%60)}:{uptime.seconds%60}"


@app.get("/uptime")
def uptime():
    return f"This is the Meshtastic Parking Lot Tracking Server For ELEE351. Server Uptime: {get_program_uptime(program_start_time)}"



@app.get("/api")
def api():
    return {
  "ParkingLotA": { "Free":random.randint(0,100), "Occupied": random.randint(0,100) },
  "ParkingLotB": { "Free": random.randint(0,100), "Occupied": random.randint(0,100)},
  "ParkingLotC": { "Free": random.randint(0,100), "Occupied": random.randint(0,100) }
}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8050) # Change 8050 to your desired portdolph