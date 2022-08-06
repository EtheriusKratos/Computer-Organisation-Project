import math

def type_1():
    global nP
    CPU_bits = int(input("Enter no of bits in CPU: "))
    change = int(input("Enter the new addressable memory option: "))
    while (change > 4 or change < 1 or change == memtype):
        print("Wrong Type.. :(")
        change = int(input("Enter the type of memory: "))
    if change == 1:
        nP += 3
    elif change == 2:
        nP += 1
    elif change == 4:
        nP +=  math.log2(CPU_bits / 8)
    print("Address pins saved of required are", P-nP)
