def decimalbinary(n, a = 10, b = 2):
    m = ""
    o = 0
    sum = 0
    nsplit = n.split(".")
    if len(nsplit) == 1:
        nsplit.append("0")
    n = nsplit[0]
    for i in n[::-1]:
        if i.isalpha() == True:
            sum += ((ord(i) - 55)) * (a ** o)
            o += 1
        else:
            sum += (int(i)) * (a ** o)
            o += 1
    while sum > 0:
        allnos = int(sum % b)
        if allnos >= 10 and allnos < 37:
            allnos = chr(55 + allnos)
        elif allnos > 36:
            print("Cant calculate for nos greater than 36...")
            return
        m += str(allnos)
        sum //= b
    return m

def A(op, reg1, reg2, reg3):
    return op + '00' + '0' * (3 - len(reg1)) + reg1 + reg2 + reg3

def B(op, reg1, Imd):
    return op + reg1 + '0' * (8 - len(Imd)) + Imd

def C(op, reg1, reg2):
    return op + '00000' + reg1 + reg2

def D(op, reg1, mem):
    return op + reg1 + '0' * (8 - len(mem)) + mem

def E(op, mem):
    return op + '000' + '0' * (8 - len(mem)) + mem

def F():
    return '0101000000000000'

dict_ISA = {"add": "10000", "sub": '10001', 'movi': '10010', 'movr': '10011', 'ld': '10100', 'st': '10101', 'mul': '10110', 'div': '10111', 'rs': '11000', 'ls': '11001', 'xor': '11010', 'or': '11011', 'and': '11100', 'not': '11101', 'cmp': '11110', 'jmp': '11111', 'jlt': '01100', 'jgt': '01101', 'je': '01111', 'hlt': '01010'}
Reg = {"R0": '000', "R1": '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110', 'FLAGS': '111'}
type_ISA = {"add": A, "sub": A, 'movi': B, 'movr': C, 'ld': D, 'st': D, 'mul': A, 'div': C, 'rs': B, 'ls': B, 'xor': A, 'or': A, 'and': A, 'not': C, 'cmp': C, 'jmp': E, 'jlt': E, 'jgt': E, 'je': E, 'hlt': F}

with open("Testcase.txt") as text:
    commands = text.readlines()
    for i in range(len(commands)):
        commands[i] = commands[i][0:(len(commands[i]) - 1)].split()
    for j in commands:
        if j[0] == 'mov' and j[2].isnumeric() == True:
           print(B(dict_ISA[j[0]], Reg[j[1]], decimalbinary(j[2][0:len(j[2])])))
        elif j[0] == 'mov':
            print(C(dict_ISA[j[0]], Reg[j[1]], Reg[j[2]]))
        else:
            if type_ISA[j[0]] == A:
                print(A(dict_ISA[j[0]], Reg[j[1]], Reg[j[2]], Reg[j[3]]))
            elif type_ISA[j[0]] == B:
                print(B(dict_ISA[j[0]], Reg[j[1]], decimalbinary(j[2][0:len(j[2])])))
            elif type_ISA[j[0]] == C:
                print(C(dict_ISA[j[0]], Reg[j[1]], Reg[j[2]]))
            elif type_ISA[j[0]] == D:
                for i in range(len(commands)):
                    if commands[i][1] == j[2]:
                        break
                print(D(dict_ISA[j[0]], Reg[j[1]], decimalbinary(str(len(commands) - i - 1))))
            elif type_ISA[j[0]] == E:
                for i in range(len(commands)):
                    if commands[i][1] == j[1]:
                        break
                print(D(dict_ISA[j[0]], decimalbinary(str(len(commands) - i - 1))))
            else:
                print(F())