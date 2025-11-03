import json
import meshtastic
from meshtastic import ble_interface, serial_interface


getAllDevices = True

filename = "devices/newNodeReference.json"


connected = False

print("Not connected...")
while not connected:
    try:
        print(" trying to connect...")
        #iface = meshtastic.ble_interface.BLEInterface('Meshtastic_01c8')
        iface = meshtastic.serial_interface.SerialInterface('')
        connected = True
    except meshtastic.ble_interface.BLEInterface.BLEError:
        pass

        print("couldn't find specified node, still tryna connect...")
print("connection successful")

n = iface.nodes

if n:
    try:
        with open(filename,'w') as f:
           json.dump(n,f,indent=4)
        f.close()
        print("done Writing")
    except IOError as e:
        print("error with file: {e}")


    if getAllDevices:
        filename = "devices/All-Devices-ids.json"
    else:
        filename = "devices/Heltec-V3-Device-ids.json"

    id: dict = dict()

    try:
        with open(filename,'r') as f:
            id = json.load(f)
        f.close()
    except FileNotFoundError:
        print("No existing Nodes to parse...")

    for i in n.values():
        sName = i["user"]["shortName"]
        if sName == "HELTEC_V3" or getAllDevices:
            if  not id.keys().__contains__(sName):
                print("found new node: " + sName + ", " + i["user"]["longName"])
            id.update({sName : i["user"]["id"]})


    try:
        with open(filename,'w') as f:
            json.dump(id, f, indent=4)
        f.close()
        print("done Writing")

    except IOError as e:
        print("error with file: {e}")






