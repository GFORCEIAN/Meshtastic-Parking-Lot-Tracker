



def updateDevices():
    num: int = 0
    conf = dict()
    conf.update({"lotConfig": {}, "serverConfig": {}, "webConfig": {}})

    while num <= 0:
        try:
            num = int(input())
            if num <= 0:
                print("please provide a number greater than zero: ", end="")
        except ValueError as e:
            print("please provide an integer: ", end="")
        except KeyboardInterrupt:
            print("traitor...")
            exit(KeyboardInterrupt())
    for i in range(1, num + 1):
        print("whats the short name of node " + str(i) + ": ", end="")
        name = input()
        print("whats the lot name " + name + " monitors?")
        lot = input()
        conf["lotConfig"].update({name: lot})
    print(conf)











