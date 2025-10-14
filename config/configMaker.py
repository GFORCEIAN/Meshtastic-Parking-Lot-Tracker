import json


def getLotConfig() -> dict:
    num: int = 0
    conf = dict({"lotConfig": {}})
    print("How many nodes do you have? ", end="")
    while num <= 0:
        try:
            num = int(input())
            if num <= 0:
                print("please provide a number greater than zero: ", end="")
        except ValueError as e:
            print("please provide an integer: ", end="")
        except KeyboardInterrupt:
            print("traitor...")
            raise KeyboardInterrupt("user aborted program")
    for i in range(1, num + 1):
        print("whats the short name of node " + str(i) + ": ", end="")
        name = input()
        print("whats the lot name " + name + " monitors?")
        lot = input()
        conf["lotConfig"].update({name: lot})
    return conf
config : dict
numCommands = 5
while True:
    op : int = 0
    try:
        with open("config.json","r") as j:
            config = json.load(j)
            j.close()
    except FileNotFoundError:
        print("no previous config found. Creating fresh config.\n")
    print("What would you like to do?\n"
          "1: update devices\n"
          "2: update server configuration\n"
          "3: update webpage configuration\n"
          "4: see current configuration\n"
          "5:exit\n"
          "> ", end="")
    while op == 0:
        try:
            op = int(input())
            if op <= 0 or op > numCommands:
                op = 0
                print("please choose a number between 1 and " + str(numCommands ) + ".")
        except ValueError:
            op = 0;
            print("please provide an integer")
    match op:
        case 1:
            config.update(getLotConfig())
            with open("config.json", "w") as w:
                json.dump(config,w,indent=4)
        case 2:
            pass
        case 3:
            pass
        case 4:
            print(json.dumps(config, indent=4))
        case 5:
            exit(0)











