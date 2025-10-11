import time
from datetime import datetime
import meshtastic
from meshtastic import ble_interface

from pubsub import pub
connected = False
interface = meshtastic.ble_interface.BLEInterface('Meshtastic_74cc')
connected = True

print("connection successful")