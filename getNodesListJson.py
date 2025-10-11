import json
import time
from datetime import datetime
from fileinput import close

import meshtastic
from meshtastic import ble_interface
from meshtastic.ble_interface import BLEInterface

from pubsub import pub

getAllDevices = True

filename = "newNodeReference.json"


connected = False

print("Not connected, trying to connect now...")
while not connected:
    try:
        iface = meshtastic.ble_interface.BLEInterface('Meshtastic_74cc')
        connected = True
    except meshtastic.ble_interface.BLEInterface.BLEError:
        print("trying to connect 74CC via bluetooth")
print("connection successful")

n = iface.nodes

if n:
    try:
        with open(filename,'w') as f:
           json.dump(n,f,indent=4)
        print("done Writing")
    except IOError as e:
        print("error with file: {e}")


    if getAllDevices:
        filename = "All-Devices-ids.json"
    else:
        filename = "Heltec-V3-Device-ids.json"

    id: dict = dict()

    try:
        with open(filename,'r') as f:
            id = json.load(f)

        for i in n.values():
            if i["user"]["hwModel"] == "HELTEC_V3" or getAllDevices:
                id.update({i["user"]["shortName"]: i["user"]["id"]})

        with open(filename,'w') as f:
            json.dump(id, f, indent=4)

        print("done Writing")
    except IOError as e:
        print("error with file: {e}")

        close()




