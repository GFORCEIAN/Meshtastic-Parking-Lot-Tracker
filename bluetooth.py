import time
from datetime import datetime
import meshtastic
from meshtastic import ble_interface

from pubsub import pub
connected = False
while(not connected):
    try:
        interface = meshtastic.ble_interface.BLEInterface('Meshtastic_74cc')
        connected = True
    except meshtastic.ble_interface.BLEInterface.BLEError:
        print("trying to connect 74CC via bluetooth")
print("connection successful")

def onReceive(packet, interface):
    try:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(packet)
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    except KeyError as e:
        print(f"Error processing packet: {e}")

    '''
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message_bytes = packet['decoded']['payload']
            message_string = message_bytes.decode('utf-8')
            print(f"{message_string} \n> ", end="", flush=True)
    except KeyError as e:
        print(f"Error processing packet: {e}")
    '''
pub.subscribe(onReceive, 'meshtastic.receive')

while(True):
    time.sleep(1)
    print("> ", end= "")
    m = input()
    print("\n")
    interface.sendText(text=m,channelIndex=2)
    print("sent message " + m)


