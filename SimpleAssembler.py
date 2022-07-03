import sys

def decimalbinary(n):
        flag=True
        if flag==True:
            num=int(n)
            if num <= 255 and num >= 0:
                ans=""
                while num>0:
                    r=str(num%2)
                    ans+=r
                    num//=2
            return (ans[::-1])

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
type_ISA = {"add": 'A', "sub": 'A', 'movi': 'B', 'movr': 'C', 'ld': 'D', 'st': 'D', 'mul': 'A', 'div': 'C', 'rs': 'B', 'ls': 'B', 'xor': 'A', 'or': 'A', 'and': 'A', 'not': 'C', 'cmp': 'C', 'jmp': 'E', 'jlt': 'E', 'jgt': 'E', 'je': 'E', 'hlt': 'F', 'var': None}

error_list = []
lista = []

#ERROR HANDLING
# with open("Testcase.txt") as text:
commands = sys.stdin.readlines()

# commands = []
# while True:
#     inp = sys.stdin.readlines()
#     commands.append(inp)
#     if inp == 'hlt':
#         break


number = 0
for i in range(len(commands)):
    commands[i] = commands[i][0:(len(commands[i]) - 1)].split()
    try:
        if commands[i][0]=='var':
            number += 1
    except:
        pass
try:
    while True:
        commands.remove([])
except:
    pass
for k in range(len(commands)):
    if commands[k][0] != "var":
        break
var_start = k + 1
for j in range(len(commands)):
    flag=0
    if(commands[j][0].find(':')!=len(commands[j][0])-1):
        try:
            if commands[j][0] == 'mov' and commands[j][2][1::].isnumeric() == True:
                try:
                    Reg[commands[j][1]]
                except:
                    error_list.append("Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                    flag = 1
                if Reg[commands[j][1]] == "111":
                    error_list.append("Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                    flag = 1
                if flag == 0 and (int(commands[j][2][1::])>127 or int(commands[j][2][1::])<0):
                    error_list.append("Error at line "+str(j+1)+": Illegal immediate values (more than 8 bits)\n")
                    flag = 1
                if flag != 1:
                    lista.append(B(dict_ISA['movi'], Reg[commands[j][1]], decimalbinary(commands[j][2][1::])) + "\n")
            elif commands[j][0] == 'mov':
                try:
                    Reg[commands[j][1]]
                    Reg[commands[j][2]]
                except:
                    error_list.append("Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                    flag = 1
                if Reg[commands[j][2]] == "111":
                    error_list.append("Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                    flag = 1
                if flag != 1:
                    lista.append(C(dict_ISA[commands[j][0]], Reg[commands[j][1]], Reg[commands[j][2]]) + "\n")
            else:
                if commands[j][0]!='mov' and commands[j][0]!='hlt' and commands[j][0]!='var':
                    try:
                        dict_ISA[commands[j][0]]
                    except:
                        error_list.append("Error at line "+str(j+1)+": Instruction name error\n")
                        flag=1
                if type_ISA[commands[j][0]] == 'A':
                    try:
                        Reg[commands[j][1]]
                        Reg[commands[j][2]]
                        Reg[commands[j][3]]
                    except:
                        error_list.append("Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                        flag = 1
                    if Reg[commands[j][1]] == "111" or Reg[commands[j][2]] == "111" or Reg[commands[j][2]] == "111":
                        error_list.append("Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                        flag = 1
                    if flag != 1:
                        lista.append(A(dict_ISA[commands[j][0]], Reg[commands[j][1]], Reg[commands[j][2]], Reg[commands[j][3]]) + "\n")
                if type_ISA[commands[j][0]] == 'B':
                    try:
                        Reg[commands[j][1]]
                    except:
                        error_list.append("Error at line "+str(j+1)+": Instruction name or register name error\n")
                        flag = 1
                    
                    if flag == 0 and (int(commands[j][2][1::])>127 or int(commands[j][2][1::])<0):
                        error_list.append("Error at line "+str(j+1)+": Illegal immediate values (more than 8 bits)\n")
                        flag = 1

                    if Reg[commands[j][1]] == "111":
                        error_list.append("Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                        flag = 1
                    if flag != 1:
                        lista.append(B(dict_ISA[commands[j][0]], Reg[commands[j][1]], decimalbinary(commands[j][2][0:len(commands[j][2])])) + "\n")
                elif type_ISA[commands[j][0]] == 'C':
                    try:
                        Reg[commands[j][1]]
                        Reg[commands[j][2]]
                    except:
                        error_list.append("Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                        flag = 1
                    if Reg[commands[j][1]] == "111" or Reg[commands[j][2]] == "111":
                        error_list.append("Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                        flag = 1
                    if flag != 1:
                        lista.append(C(dict_ISA[commands[j][0]], Reg[commands[j][1]], Reg[commands[j][2]])+ "\n")
                elif type_ISA[commands[j][0]] == 'D':
                    try:
                        Reg[commands[j][1]]
                    except:
                        error_list.append("Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                        flag = 1
                    if Reg[commands[j][1]] == "111":
                        error_list.append("Error at line "+str(j+1)+": "+"Illegal use of Flags register\n")
                        flag = 1
                    choice = False
                    for i in range(len(commands)-1):
                        if commands[i][1] == commands[j][2]:
                            choice = True
                            break
                        elif commands[i][0][:-1] == commands[j][2]:
                            choice = "labelused"
                            break
                    if choice==False:
                        error_list.append("Error at line "+str(j+1)+": "+"Use of undefined variable(s)\n")
                    elif choice == "labelused":
                        error_list.append("Error at line "+str(j+1)+": "+"Misuse of label as variable\n")
                    if i >= var_start:
                        error_list.append("Error at line "+str(j+1)+": "+"Variable not declared at the beginning\n")
                        flag = 1
                    if flag != 1 and choice == True:
                        lista.append(D(dict_ISA[commands[j][0]], Reg[commands[j][1]], decimalbinary(str(len(commands) - i - 1))) + "\n")
                elif type_ISA[commands[j][0]] == 'E':
                    choice = False
                    for i in range(len(commands)-1):
                        if commands[i][0][:-1] == commands[j][1]:
                            choice = True
                            break
                        elif commands[i][1] == commands[j][1]:
                            choice = "variableused"
                            break
                    if choice==False:
                        error_list.append("Error at line "+str(j+1)+": "+"Use of undefined label(s)\n")
                    elif choice == "variableused":
                        error_list.append("Error at line "+str(j+1)+": "+"Misuse of variable as label\n")
                    if i >= var_start:
                        error_list.append("Error at line "+str(j+1)+": "+"Variable not declared at the beginning\n")
                        flag = 1
                    if flag != 1 and choice == True:
                        lista.append(D(dict_ISA[commands[j][0]], decimalbinary(str(len(commands) - i - 1))) + "\n")
                elif type_ISA[commands[j][0]] == 'F':
                    lista.append(F() + "\n")
        except:
            if flag == 0:
                error_list.append("Syntax error in line " + str(j + 1) + "\n")
    else:
        achecker = commands[j]
        commands[j] = commands[j][1:]
        try:
            if commands[j][0] == 'mov' and commands[j][2][1::].isnumeric() == True:
                try:
                    Reg[commands[j][1]]
                except:
                    error_list.append("Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                    flag = 1
                if Reg[commands[j][1]] == "111":
                    error_list.append("Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                    flag = 1
                if flag == 0 and (int(commands[j][2][1::])>127 or int(commands[j][2][1::])<0):
                    error_list.append("Error at line "+str(j+1)+": Illegal immediate values (more than 8 bits)\n")
                    flag = 1
                if flag != 1:
                    lista.append(B(dict_ISA['movi'], Reg[commands[j][1]], decimalbinary(commands[j][2][1::])) + "\n")
            elif commands[j][0] == 'mov':
                try:
                    Reg[commands[j][1]]
                    Reg[commands[j][2]]
                except:
                    error_list.append("Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                    flag = 1
                if Reg[commands[j][2]] == "111":
                    error_list.append("Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                    flag = 1
                if flag != 1:
                    lista.append(C(dict_ISA[commands[j][0]], Reg[commands[j][1]], Reg[commands[j][2]]) + "\n")
            else:
                if commands[j][0]!='mov' and commands[j][0]!='hlt' and commands[j][0]!='var':
                    try:
                        dict_ISA[commands[j][0]]
                    except:
                        error_list.append("Error at line "+str(j+1)+": Instruction name error\n")
                        flag=1
                if type_ISA[commands[j][0]] == 'A':
                    try:
                        Reg[commands[j][1]]
                        Reg[commands[j][2]]
                        Reg[commands[j][3]]
                    except:
                        error_list.append("Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                        flag = 1
                    if Reg[commands[j][1]] == "111" or Reg[commands[j][2]] == "111" or Reg[commands[j][2]] == "111":
                        error_list.append("Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                        flag = 1
                    if flag != 1:
                        lista.append(A(dict_ISA[commands[j][0]], Reg[commands[j][1]], Reg[commands[j][2]], Reg[commands[j][3]]) + "\n")
                if type_ISA[commands[j][0]] == 'B':
                    try:
                        Reg[commands[j][1]]
                    except:
                        error_list.append("Error at line "+str(j+1)+": Instruction name or register name error\n")
                        flag = 1
                    
                    if flag == 0 and (int(commands[j][2][1::])>127 or int(commands[j][2][1::])<0):
                        error_list.append("Error at line "+str(j+1)+": Illegal immediate values (more than 8 bits)\n")
                        flag = 1

                    if Reg[commands[j][1]] == "111":
                        error_list.append("Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                        flag = 1
                    if flag != 1:
                        lista.append(B(dict_ISA[commands[j][0]], Reg[commands[j][1]], decimalbinary(commands[j][2][0:len(commands[j][2])])) + "\n")
                elif type_ISA[commands[j][0]] == 'C':
                    try:
                        Reg[commands[j][1]]
                        Reg[commands[j][2]]
                    except:
                        error_list.append("Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                        flag = 1
                    if Reg[commands[j][1]] == "111" or Reg[commands[j][2]] == "111":
                        error_list.append("Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                        flag = 1
                    if flag != 1:
                        lista.append(C(dict_ISA[commands[j][0]], Reg[commands[j][1]], Reg[commands[j][2]])+ "\n")
                elif type_ISA[commands[j][0]] == 'D':
                    try:
                        Reg[commands[j][1]]
                    except:
                        error_list.append("Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                        flag = 1
                    if Reg[commands[j][1]] == "111":
                        error_list.append("Error at line "+str(j+1)+": "+"Illegal use of Flags register\n")
                        flag = 1
                    choice = False
                    for i in range(len(commands)-1):
                        if commands[i][1] == commands[j][2]:
                            choice = True
                            break
                        elif commands[i][0][:-1] == commands[j][2]:
                            choice = "labelused"
                            break
                    if choice==False:
                        error_list.append("Error at line "+str(j+1)+": "+"Use of undefined variable(s)\n")
                    elif choice == "labelused":
                        error_list.append("Error at line "+str(j+1)+": "+"Misuse of label as variable\n")
                    if i >= var_start:
                        error_list.append("Error at line "+str(j+1)+": "+"Variable not declared at the beginning\n")
                        flag = 1
                    if flag != 1 and choice == True:
                        lista.append(D(dict_ISA[commands[j][0]], Reg[commands[j][1]], decimalbinary(str(len(commands) - i - 1))) + "\n")
                elif type_ISA[commands[j][0]] == 'E':
                    choice = False
                    for i in range(len(commands)-1):
                        if commands[i][0][:-1] == commands[j][1]:
                            choice = True
                            break
                        elif commands[i][1] == commands[j][1]:
                            choice = "variableused"
                            break
                    if choice==False:
                        error_list.append("Error at line "+str(j+1)+": "+"Use of undefined label(s)\n")
                    elif choice == "variableused":
                        error_list.append("Error at line "+str(j+1)+": "+"Misuse of variable as label\n")
                    if i >= var_start:
                        error_list.append("Error at line "+str(j+1)+": "+"Variable not declared at the beginning\n")
                        flag = 1
                    if flag != 1 and choice == True:
                        lista.append(D(dict_ISA[commands[j][0]], decimalbinary(str(len(commands) - i - 1))) + "\n")
                elif type_ISA[commands[j][0]] == 'F':
                    lista.append(F() + "\n")
        except:
            if flag == 0:
                error_list.append("Syntax error in line " + str(j + 1) + "\n")
check = False
for k in commands:
    if len(k) > 0 and k[0] == 'hlt':
        check = True
        break
if check == False:
    error_list.append("Missing Halt instruction\n")
if commands[-1][0] != 'hlt':
    print(list(commands[-1]))
    error_list.append("Halt not being used as last instruction\n")


with open("OutputText.txt", 'w') as writer:
    if (len(error_list) == 0):
        for i in lista:
            print(i, end = "")
    else:
        for i in error_list:
            print(i, end = "")