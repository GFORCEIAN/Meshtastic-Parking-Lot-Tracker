import meshtastic.serial_interface
from pubsub import pub

interface = meshtastic.serial_interface.SerialInterface()


def interpret(s: str):
    msg = s.split(',')
    match(msg[0]):
        case "L": #Update Lot Counts
            pass #do nothing for now

        case "B": #update Battery Monitoring CSV
            pass # do nothing for now

        case "E": #log error condition
            pass # do nothing for now







def onReceive(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message_bytes = packet['decoded']['payload']
            message_string = message_bytes.decode('utf-8')
            print(message_string)

            interpret(message_string)
    except KeyError as e:
        print(f"Error processing packet: {e}")

pub.subscribe(onReceive, 'meshtastic.receive')

def send_message(message):
    interface.sendText(message)

while True:
    text = input("> ")
    send_message(text)