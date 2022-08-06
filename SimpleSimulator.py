import string
import sys
from glob import glob
import opcode
from matplotlib.axis import YAxis
import matplotlib.pyplot as plt
import numpy as np


def binary_to_float(s):
    t = s.split('.')
    return int(t[0], 2) + int(t[1], 2) / 2.**len(t[1])

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

def cse_to_binary(x):
    exponent=int(x[:3],2)
    return "1"+x[3:][:exponent]+"."+x[3:][exponent:]
    

regs_val=[]
for i in range(7):
    regs_val.append(0)
flag=[0,0,0,0]
regs_val.append(flag)

halt=False
def print_regs(y):
    print(bin(y)[2:].zfill(8), end=" ")
    for i in regs_val[0:7]:
        if type(i)!=int:
            print(8*"0"+binary_to_cse(floating_to_binary(str(i))),end=" ")
        else:
            print (bin(i)[2:].zfill(16), end=" ")
    x=""
    for i in regs_val[7]:
        x+=str(i)
    print(12*"0"+x)
memory=[]
for i in range(256):
  memory.append(0)
def memory_dump():
    global memory
    for i in memory:
        if(type(i)==str):
            print(i)
        if(type(i)==float):
            print(8*"0"+cse_to_binary(floating_to_binary(str(i))))
        if (type(i)==int):
            print(bin(i)[2:].zfill(16))
def addf(x,y):
    return overflow_f(x+y)

def subf(x,y):
    return overflow_f(y-x)

def add(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    return overflow(x+y)

def sub(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    return overflow(y-x)
  
def div(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    global regs_val
    regs_val[0]=(x//y)
    regs_val[1]=x%y

def cmp(x,y):
    global regs_val
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    if(x<y):
        regs_val[7][1]=1
    elif (x>y):
        regs_val[7][2]=1
    elif(x==y):
        regs_val[7][3]=1

def mul(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    return overflow(x*y)

def Xor(x,y):
    return x^y
def OR(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    return x|y

def AND(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    return x&y

def NOT(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    x=[i for i in bin(x)[2:].zfill(16)]
    z=""
    for i in range(len(x)):
        if(x[i]=="1"):
            x[i]="0"
        else:
            x[i]="1"
        z+=x[i]
    return int(z,2)
def rs(x,imm):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    return x>>imm
def ls(x,imm):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    return x<<imm
def mov(y,x):
    return x

def movf(y,x):
    return x


def ld(x,mem):
    global regs_val
    regs_val[x]=memory[mem]

def st(x,mem):
    memory[mem]=regs_val[x]
    

def jgt(address):
  if(regs_val[7][2]==1):
    return(address)
  else:
    return -1
def jet(address):
  if(regs_val[7][3]==1):
    return address
  else:
    return -1
def jlt(address):
  if(regs_val[7][1]==1):
    return address
  else:
    return -1
def jmp(address):
  return address

def hlt():
  global halt
  halt=True
  return halt

op_code={
    "00000":[addf,"A",False],
    "00001":[subf,"A",False],
    "10000":[add,"A",False],
    "10001":[sub,"A",False],
    "10110":[mul,"A",False],
    "11010":[Xor,"A",False],
    "11011":[OR,"A",False],
    "11100":[AND,"A",False],
    "00010":[movf,"B",False],
    "10010":[mov,"B",False],
    "11000":[rs,"B",False],
    "11001":[ls,"B",False],
    "10011":[mov,"C",False],
    "10111":["div","C",False],
    "11101":[NOT,"C",False],
    "11110":["cmp","C",True],
    "10100":[ld,"D",False],
    "10101":[st,"D",False],
    "11111":[jmp,"E",False],
    "01100":[jlt,"E",False],
    "01101":[jgt,"E",False],
    "01111":[jet,"E",False],
    "01010":[hlt,"F",False],
    
}
reg_code={
    "000":0,
    "001":1,
    "010":2,
    "011":3,
    "100":4,
    "101":5,
    "110":6,
    "111":7
}
