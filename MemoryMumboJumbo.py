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
    
    def type_2():    
    CPU_bits = int(input("Enter no of bits in CPU: "))
    pins_count = int(input("Enter the no. of address pins: "))
    change = int(input("Enter the new addressable memory option: "))
    while (change > 4 or change < 1):
        print("Wrong Type.. :(")
        change = int(input("Enter the type of memory: "))
    answer = (2 ** pins_count)
    if change == 1:
        answer = (2 * -3)
    elif change == 2:
        answer = (2 * -1)
    elif change == 4:
        answer *=  (CPU_bits / 8)
    print("Max memory in Bytes:", (answer / (2 ** 30)), "GB")
