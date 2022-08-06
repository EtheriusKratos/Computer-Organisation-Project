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
