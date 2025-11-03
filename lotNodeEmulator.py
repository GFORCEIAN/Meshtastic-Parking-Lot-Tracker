import time
from datetime import datetime
import meshtastic
# from Tools.scripts.texi2html import increment
from meshtastic import ble_interface, serial_interface
from pubsub import pub



def getNum() -> int:
    num: int
    gotNum= False
    while not gotNum:
        try:
            s : str = input()
            if(s == "e"):
                print("see ya later alligator 🐊")
                exit(0)
            num = int(s)
            gotNum = True
        except ValueError as e:
            print("please provide an integer: ", end="")
        except KeyboardInterrupt:
            print("traitor...")
            raise KeyboardInterrupt("user aborted program")
    return num

connected = False
while(not connected):
    try:
        #interface = meshtastic.ble_interface.BLEInterface('Meshtastic_01c8')
        interface = meshtastic.serial_interface.SerialInterface()

        connected = True
    except meshtastic.ble_interface.BLEInterface.BLEError:
        print("trying to connect 01c8 via bluetooth")
print("connection successful")

def onReceive(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message_bytes = packet['decoded']['payload']
            message_string = message_bytes.decode('utf-8')
            print(f"{message_string} \n> ", end="", flush=True)
    except KeyError as e:
        print(f"Error processing packet: {e}")

pub.subscribe(onReceive, 'meshtastic.receive')
numCommands = 4
while(True):
    op: int = 0
    print("What would you like to do?\n"
          "1: Send HeartBeat ❤️\n"
          "2: Update Lot Count\n"
          "3: Set Lot Count\n"
          "4: send data to webapge --> WIP\n"
          "Enter \"e\" to exit at any time\n"
          "> ", end="")

    while op == 0:
        try:
            op = getNum()
            if op <= 0 or op > numCommands:
                op = 0
                print("Please choose a number between 1 and " + str(numCommands) + ".")
        except ValueError:
            op = 0
            print("please provide an integer")
    shouldSend = True
    match op:
        case 1:
            m = "❤️"
        case 2:
            print("did the car enter or leave?\n"
                  "1: enter\n"
                  "2: leave")
            n = getNum()
            if n == 1:
                m = "L,Lot North,enter"
            elif n == 2:
                m = "L,Lot North,leave"
            elif n == 3:
                print("bad")
                shouldSend = False

        case 3:
            pass
            # updateConfigFile(getServerConfig())
        case 4:
            pass
            # updateConfigFile(getWebServerConfig())
        case 5:
            pass
    #
    if shouldSend == True:
        interface.sendText(text=m, channelIndex=2)
        print(f"sent text: {m}\n\n")
