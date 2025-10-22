import meshtastic.serial_interface
from pubsub import pub

interface = meshtastic.serial_interface.SerialInterface("/dev/ttyS0")


def interpret(s: str, fromId):
    msg = s.split(',')
    print("Message from ("+fromId+"): " + str(msg))
    match(msg[0]):
        case "L": #Update Lot Counts
            pass #do nothing for now

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