import json
import os
import time

import meshtastic.serial_interface
from pubsub import pub
from jsonParser import readJsonFile
import WebserverTester
from csv_logger_test import ParkingLog
import threading
import platform


interface : meshtastic.serial_interface.SerialInterface
nodeConnected:bool = True

def start_webserver():
    import uvicorn
    uvicorn.run(WebserverTester.app,log_level="warning", host="0.0.0.0", port=8050)

config: dict = readJsonFile("config/config.json")


custom_lots_dict = config.get("lotConfig")
#print(custom_lots_dict)

custom_lots = list(custom_lots_dict.keys())

custom_status = {
    "Lot North": (20, 100),  # 20 cars currently, 100 max
    "Lot East": (55, 60),  # 55/60
    "Lot West": (0, 40)  # 0/40
}

logger = ParkingLog(filename="parking_log.csv", lots=custom_lots, initial_counts=custom_status)
from WebserverTester import set_logger
set_logger(logger)


# Create your parking logger with custom setup
def main():
    global interface
    web_thread = threading.Thread(target=start_webserver, daemon=True)
    web_thread.start()
    print("Web server started on port 8050")

    # switch depending on if ian's computer or pi
    # interface = meshtastic.serial_interface.SerialInterface("/dev/ttyUSB0")

    if nodeConnected:
        HostName = platform.uname()[1]
        if HostName == "IUseArchByTheWay":
            interface = meshtastic.serial_interface.SerialInterface("/dev/ttyUSB0")
        else:
            interface = meshtastic.serial_interface.SerialInterface("/dev/ttyS0")
        pub.subscribe(onReceive, 'meshtastic.receive')

        print("""Commands:\n
        exit -> exit program\n
        s<text> -> send message\n
        u<lot_string,count_int> -> update lot count e.g  u(enter) Lot North (enter) 10 (enter) """)

        updateWebSite()
        # main loop
        while True:
            text:str = input("> ")
            if text == "exit":
                # any cleanup code can goes here or after the while loop
                interface.close()
                print("Serial closed")
                break
            if len(text) > 0:
                c = text[0]#get command type
                match c:
                    case "s":
                        send_message(input("What woould you like to send? "))
                    case "u":
                        try:
                            setLotCount(input("Which lot? "),int(input("How many cars? ")))
                            updateWebSite()
                        except Exception as w:
                            print(w)
                    case _:
                        print("bad input")

                




def interpret(s: str, fromId):
    msg = s.split(',')
    print("Message from ("+fromId+"): " + str(msg))
    match(msg[0]):
        case "L": #Update Lot Counts
            if len(msg) < 3:
                print("Invalid lot message format >:O. Expected: L,<lot_name>,<enter/leave>")
                return
            lot_name = msg[1].strip()
            action = msg[2].strip().lower()

            print(f"Lot update received: {lot_name} -> {action}")
            logger.update_lot(lot_name, action)
            logger.get_lot_status()


        case "B": #update Battery Monitoring CSV
            print("got bat info")
            pass # do nothing for now

        case "W": #log warning condition
            if len(msg) != 3:
                print("Invalid warning format")
            warningMessage:str = msg[1]
            id:int = int(msg[2])

            print(f"Warning ({id}): {warningMessage}")
            send_message(f"WR,{id}")
            pass # do nothing for now

        case "❤️":
            # heart beat, relpy with beating heart
            send_message("💓")
            pass
        case _:
            pass


def onReceive(packet:dict, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP' and packet.get("channel", 0) == 2:
            message_bytes = packet['decoded']['payload']
            from_bytes = packet['fromId']
            message_string = message_bytes.decode('utf-8')
            # print(message_string)
            # print(from_bytes)

            interpret(message_string, from_bytes)
    except KeyError as e:
        print(f"Error processing packet: {e}")

def send_message(message:str):
    interface.sendText(message, channelIndex=2, destinationId="!433b01c8", wantResponse=True)

def setLotCount(lotname:str, count: int):
    custom_lots_dict.get(lotname)[1] = count
    print("Set " + lotname + " to " + str(count) + " cars.")
def getLotCount(lotname:str) -> int:
    lotList = config.get(lotname)
    return lotList[2] - lotList[1]
def updateWebSite():
    webLots:list = []
    for lot in custom_lots:
        lotList = custom_lots_dict.get(lot)
        counts:tuple[int,int,str] = (lotList[1],lotList[2],lot)
        webLots.append(counts)
    #print(webLots)
    WebserverTester.setLots(webLots)


try:
    main()
finally:
    with open("config/config.json", "w") as w:
        #print(config)
        json.dump(config, w, indent=4)