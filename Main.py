import meshtastic.serial_interface
from pubsub import pub

from csv_logger_test import ParkingLog

interface = meshtastic.serial_interface.SerialInterface("/dev/ttyS0")

custom_lots = ["Lot North", "Lot East", "Lot West"]
custom_status = {
    "Lot North": (20, 100),  # 20 cars currently, 100 max
    "Lot East": (55, 60),  # 55/60
    "Lot West": (0, 40)  # 0/40
}
# Create your parking logger with custom setup
logger = ParkingLog(filename="parking_log.csv", lots=custom_lots, initial_counts=custom_status)

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

        case "E": #log error condition
            pass # do nothing for now







def onReceive(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message_bytes = packet['decoded']['payload']
            from_bytes = packet['fromId']
            message_string = message_bytes.decode('utf-8')
            # print(message_string)
            # print(from_bytes)

            interpret(message_string, from_bytes)
    except KeyError as e:
        print(f"Error processing packet: {e}")

    

pub.subscribe(onReceive, 'meshtastic.receive')

def send_message(message):
    interface.sendText(message, channelIndex=2)

while True:
    text = input("> ")
    send_message(text)