import sys


var = {}
labels = {}

def floating_to_binary(x):
    integer=int(x.split(".")[0])
    floating=int(x.split(".")[1])
    binary=str(bin(integer)[2:])+"."
    decimal="0."+str(floating)
    decimal=float(decimal)
    result=""
    for i in range(5):
        decimal=decimal*2
        result+=str(decimal).split(".")[0]
        decimal=float("."+(str(decimal).split(".")[1]))
    return binary+result


def binary_to_cse(x):
    ans=""
    exponent=len((x.split(".")[0]))-1
    ans=str(bin(exponent)[2:].zfill(3))+(x.split(".")[0][1:]+(x.split(".")[1]))[:5]
    return ans


def decimalbinary(x):
    if (str(x).count(".") == 0):
        return bin(int(x))[2:]
    else:
        ans=""
        exponent=len((x.split(".")[0]))-1
        ans=str(bin(exponent)[2:].zfill(3))+(x.split(".")[0][1:]+(x.split(".")[1]))[:5]
        return ans

############# binary encoding #############
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

############# declaring dictionaries #############
dict_ISA = {"addf": "00000", "subf": "00001", "movf": "00010" ,"add": "10000", "sub": '10001', 'movi': '10010', 'movr': '10011', 'ld': '10100', 'st': '10101', 'mul': '10110', 'div': '10111', 'rs': '11000', 'ls': '11001', 'xor': '11010', 'or': '11011', 'and': '11100', 'not': '11101', 'cmp': '11110', 'jmp': '11111', 'jlt': '01100', 'jgt': '01101', 'je': '01111', 'hlt': '01010'}
Reg = {"R0": '000', "R1": '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110', 'FLAGS': '111'}
type_ISA = {"addf": "A", "subf": "A", "movf": "B" ,"add": 'A', "sub": 'A', 'movi': 'B', 'movr': 'C', 'ld': 'D', 'st': 'D', 'mul': 'A', 'div': 'C', 'rs': 'B', 'ls': 'B', 'xor': 'A', 'or': 'A', 'and': 'A', 'not': 'C', 'cmp': 'C', 'jmp': 'E', 'jlt': 'E', 'jgt': 'E', 'je': 'E', 'hlt': 'F', 'var': None}
############# storing output #############
# For storing error lines
error_list = []
# For storing correct lines
lista = []


############# inputting #############
commands = sys.stdin.readlines()
# f = open(
#     "../automatedTesting/tests/assembly/hardBin/{}".format(sys.argv[1]), "r")
# commands = f.readlines()
# f.close()


def convert(j):
    global flag
    global _CommandResults
    global lista, error_list
    global Reg
    global var
    try:
    # for mov imm
    # print(commands[j][0])
    # print((list(commands[j][2][1::])).remove("."))
    #print(commands[j][2][0])

        if (commands[j][0] == 'movf'):
            a = list(commands[j][2][1::])
            a.remove(".")
            a = "".join(a)
        if (commands[j][0] == 'mov' or commands[j][0] == 'movf') and (commands[j][2][1::].isnumeric() == True or (a).isnumeric() == True) and commands[j][2][0] == "$":
            try:
                Reg[commands[j][1]]
            except:
                error_list.append(
                    "Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                flag = 1
            if Reg[commands[j][1]] == "111":
                error_list.append(
                    "Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                flag = 1
            if commands[j][0]!="movf" and flag == 0 and (int(commands[j][2][1::]) > 256 or int(commands[j][2][1::]) < 0):
                error_list.append(
                    "Error at line "+str(j+1)+": Illegal immediate values (more than 8 bits)\n")
                flag = 1
            if(commands[j][0]=="movf"):
                if(flag==0 and float((commands[j][2][1::]))>int('11111100',2) or float((commands[j][2][1::]))<1.0):
                    error_list.append("Error at line "+str(j+1)+": Illegal immediate value for floating integer\n")
                    flag=1
                if flag!=1:
                    lista.append(B(dict_ISA[commands[j][0]], Reg[commands[j][1]], binary_to_cse(floating_to_binary((commands[j][2][1:len(commands[j][2])])))) + "\n")
            if commands[j][0] != "movf" and flag != 1:
                lista.append(B(dict_ISA['movi'], Reg[commands[j][1]], decimalbinary(
                    commands[j][2][1::])) + "\n")
