import meshtastic.serial_interface
from pubsub import pub

interface : meshtastic.serial_interface.SerialInterface

def main():
    global interface
    interface = meshtastic.serial_interface.SerialInterface("/dev/ttyS0")

    pub.subscribe(onReceive, 'meshtastic.receive')

    # main loop
    while True:
        text = input("> ")
        if (text == "exit"):
            # any cleanup code can goes here or after the while loop
            interface.close()
            print("Serial closed")
            break
        send_message(text)


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

        case "❤️":
            # heart beat
        
            pass
        case _:
            pass


def onReceive(packet:dict, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP' and packet.get("channel", 0) == 2:
            message_bytes = packet['decoded']['payload']
            from_bytes = packet['fromId']
            message_string = message_bytes.decode('utf-8')

            interpret(message_string, from_bytes)
    except KeyError as e:
        print(f"Error processing packet: {e}")

def send_message(message:str):
    interface.sendText(message, channelIndex=2, destinationId="!433b01c8", wantResponse=True)






main()