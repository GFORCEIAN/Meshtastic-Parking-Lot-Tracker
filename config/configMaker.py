from logging import exception

print("How Many Nodes do you Have? ", end="")
num : int = 0
while num <= 0:
    try:
        num = int(input())
        if num <= 0:
            print("please provide a number greater than zero", end="")
    except ValueError as e:
        print("please provide an integer: ", end="")


