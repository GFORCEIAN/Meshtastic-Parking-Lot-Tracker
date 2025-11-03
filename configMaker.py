import json
from jsonParser import readJsonFile

defaultConf = {"lotConfig" : {},
               "serverConfig" : {},
               "webServerConfig" : {}
               }


config : dict


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

def getLotConfig() -> dict:
    num: int = 0
    max: int = 20
    conf = dict({"lotConfig": {}})
    print("How many nodes do you have? ", end="")
    while num <= 0:
        num = getNum()
        if num <= 0 or num > max:
            print("please provide a number greater than zero and less than " + str(max + 1) + ": ", end="")
            num = 0

    for i in range(1, num + 1):
        print("whats the short name of node " + str(i) + ": ", end="")
        name = input()

        decision : str = input("Would you like to use a cached value for the ID?  Y/n: ").lower()

        if decision != "" and decision != "y":
            print("whats the ID of the node " + str(i) + ": ", end="")
            id = input()
        else:
            idJson : dict = readJsonFile("devices/Heltec-V3-Device-ids.json")
            id: str = idJson.get(name,None)
            if (id != None):
                print("using cached value " +id)
            else:
                print("id not found, writing: \"\"")
        print("whats the lot name " + name + " monitors?")
        lot = input()

        conf["lotConfig"].update({lot: (name, id)})
    return conf



def getServerConfig() -> dict:
    pass


def getWebServerConfig() -> dict:
    pass

def updateConfigFile(newConf : dict) -> None:
    config.update(newConf)
    with open("config/config.json", "w") as w:
        json.dump(config, w, indent=4)


def removeDevice(s: str) -> None:
    config["lotConfig"].pop(s)
    updateConfigFile(config)

numCommands = 5
while True:
    op : int = 0
    try:
        with open("config/config.json", "r") as j:
            config = json.load(j)
            j.close()
    except FileNotFoundError:
        print("no previous config found. Creating fresh config.\n")
        config = defaultConf
        updateConfigFile(config)
    print("What would you like to do?\n"
          "1: Update devices\n"
          "2: Remove devices\n"
          "3: Update server configuration\n"
          "4: Update webpage configuration\n"
          "5: See current configuration\n"
          "Enter \"e\" to exit at any time\n"
          "> ", end="")
    while op == 0:
        try:
            op = getNum()
            if op <= 0 or op > numCommands:
                op = 0
                print("Please choose a number between 1 and " + str(numCommands ) + ".")
        except ValueError:
            op = 0
            print("please provide an integer")
    match op:
        case 1:
            updateConfigFile(getLotConfig())
        case 2:
            s = input("Whats the name of the device you want to remove? ")
            if config["lotConfig"].keys().__contains__(s):
                removeDevice(s)
                print("\nRemoved: " + s + " from the configuration.\n")
            else:
                print("\nThat device was not Found in the current configuration.\n")
        case 3:
            pass
            #updateConfigFile(getServerConfig())
        case 4:
            pass
            #updateConfigFile(getWebServerConfig())
        case 5:
            print(json.dumps(config, indent=4))












