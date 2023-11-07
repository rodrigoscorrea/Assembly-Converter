"""
Author: Rodrigo Santos Correa
Objective: Computer Organization Subject
"""
#Required imports

from ast import arguments
import sys
import re

args = sys.argv

#Auxiliary functions

def bin(reg, n): 
    reg = reg.group(n)
    reg = "{0:02b}".format(int(reg))
    return reg

def hexOp1(op, reg, n):
    reg = bin(reg, n)
    operation = hex(int(op + reg, 2))[2:]
    return operation

def hexOp2(op, regs):
    R1 = bin(regs, 1)
    R2 = bin(regs, 2)
    operation = op + R1 + R2
    operation = hex(int(operation, 2))[2:]
    return operation

def read_inputfile(assembly_file):

    # Regular expressions creation
    reg_move = r"move r([0-9]+),\s*r([0-9])"
    reg_halt = r"halt$"
    reg_code = r"^\.code$"
    reg_data = r"^\.data$"
    reg_word = r"word\s+([0-9A-Fa-fx]+)"
    reg_comment = "( +;{1} +.*)?"
    reg_start = "^"
    reg_geral = r"\sR([0-9]+),\s*R([0-9]+)( +#{1}.*)?"
    reg_ula = ["ADD", "SHR", "SHL", "NOT", "AND", "OR", "XOR", "CMP", "LD", "ST"]
    reg_not_ula = [ 
            r"DATA R([0-9]+)\s*,\s*0x([A-F0-9]+)",
            r"OUT addr,\s*R([0-9]+)", r"OUT data,\s*R([0-9]+)",
            r"IN addr,\s*R([0-9]+)", r"IN data,\s*R([0-9]+)",
            "CLF",
            "JMP ((0x)?[A-F0-9]+)",
            "J{1}(C?)(A?)(E?)(Z?) (((0x)?[A-F0-9]+)?)",
            r"JMPR R([0-9]+)",
            r"DATA R([0-9]+)\s*,\s*([0-9]+)"]

    hex_list = []

    # Compare input file data with the regular expressions
    with open(assembly_file, "r") as arquivo:
        code = False
        data = False
        halt = False
        move = False
        for line in arquivo:
            line = line.strip()
            if not code:
                prog = re.compile(reg_code, re.IGNORECASE) #sensitive case disabled
                result = prog.match(line)
                if result is not None: #aknowledge .code section
                    code = True
            if not data:
                prog = re.compile(reg_data, re.IGNORECASE)
                result = prog.match(line)
                if result is not None: #aknowledge .data section
                    data = True
            if not halt:
                prog = re.compile(reg_halt, re.IGNORECASE)
                result = prog.match(line)
                if result is not None: #aknowledge word "halt"
                    halt = True        
            if not move:
                prog = re.compile(reg_move, re.IGNORECASE)
                result = prog.match(line)
                if result is not None:  #aknowledge word "move"
                    move = True
            if code:
                sucesso = False
                number = 0
                for expression in reg_ula: #reads the expressionstrying to fit them into the ALU operations
                    total = reg_start + expression + reg_geral
                    recomp = re.compile(total, re.IGNORECASE)
                    result = recomp.match(line)
                    if result is not None:
                        if (number >= 0 and number <= 9):
                            match number:
                                case 0:
                                    ADD = hexOp2("1000", result)
                                    hex_list.append(ADD)
                                case 1:
                                    SHR = hexOp2("1001", result)
                                    hex_list.append(SHR)
                                case 2:
                                    SHL = hexOp2("1010", result)
                                    hex_list.append(SHL)
                                case 3:
                                    NOT = hexOp2("1011", result)
                                    hex_list.append(NOT)
                                case 4:
                                    AND = hexOp2("1100", result)
                                    hex_list.append(AND)
                                case 5:
                                    OR = hexOp2("1101", result)
                                    hex_list.append(OR)
                                case 6:
                                    XOR = hexOp2("1110", result)
                                    hex_list.append(XOR)
                                case 7:
                                    CMP = hexOp2("1111", result)
                                    hex_list.append(CMP)
                                case 8:
                                    LD = hexOp2("0000", result)
                                    LD = "{:02x}".format(int(LD, 16))
                                    hex_list.append(LD)
                                case 9:
                                    ST = hexOp2("0001", result)
                                    hex_list.append(ST)
                        sucesso = True
                        break
                    number += 1
                if (not sucesso):    #Deals with non ALU operations
                    for expression in reg_not_ula:
                        ex = reg_start + expression + reg_comment
                        recomp = re.compile(ex, re.IGNORECASE)
                        result = recomp.match(line)
                        if result is not None:
                            if (number > 9 and number <=19):
                                match number:
                                    case 10:
                                        hexa = result.group(2)
                                        DATA = hexOp1("001000", result, 1)
                                        hex_list.append(DATA)
                                        hex_list.append(hexa)
                                    case 11:
                                        OUT = hexOp1("011111", result, 1)
                                        hex_list.append(OUT)
                                    case 12:
                                        OUT = hexOp1("011110", result, 1)
                                        hex_list.append(OUT)
                                    case 13:
                                        IN = hexOp1("011101", result, 1)
                                        hex_list.append(IN)
                                    case 14:
                                        IN = hexOp1("011100", result, 1)
                                        hex_list.append(IN)
                                    case 15:
                                        CLF = "60"
                                        hex_list.append(CLF)
                                    case 16:
                                        JMP = "40"
                                        FLAG = result.group(1)
                                        if (FLAG in hex_list) :
                                            LOOP = int(hex_list.index(FLAG))
                                            hex_list.pop(LOOP)
                                            LOOP = hex(LOOP)[2:].zfill(2)
                                            
                                            hex_list.append(JMP)
                                            hex_list.append(LOOP)
                                        else:
                                            hex_list.append(JMP)
                                            if(FLAG.startswith("0x")):
                                                hex_list.append(FLAG[2:])
                                            else:
                                                FLAG = int(FLAG)
                                                FLAG = hex(FLAG)
                                                hex_list.append(FLAG[2:])
                                    case 17:
                                        JCAEZ = "0101"
                                        FLAGS = "1" if result.group(1) != "" else "0"
                                        FLAGS = FLAGS + "1" if result.group(2) != "" else FLAGS + "0"
                                        FLAGS = FLAGS + "1" if result.group(3) != "" else FLAGS + "0"
                                        FLAGS = FLAGS + "1" if result.group(4) != "" else FLAGS + "0"
                                        JCAEZ = JCAEZ + FLAGS
                                        JCAEZ = hex(int(JCAEZ,2))[2:]
                                        FLAG = result.group(5)
                                        if (FLAG in hex_list) :
                                            LOOP = int(hex_list.index(FLAG))
                                            hex_list.pop(LOOP)
                                            LOOP = hex(LOOP)[2:].zfill(2)
                                            hex_list.append(JCAEZ)
                                            hex_list.append(LOOP)
                                        else:
                                            hex_list.append(JCAEZ)
                                            if(FLAG.startswith("0x")):
                                                FLAG = FLAG[2:]
                                                hex_list.append(FLAG)
                                            else:
                                                FLAG = hex(int(FLAG))
                                                hex_list.append(FLAG[2:])
                                    case 18:
                                        FLAG = result.group(1)
                                        FLAG = '3' + FLAG
                                        hex_list.append(FLAG)
                                    case 19:
                                        data = '2'
                                        reg = result.group(1)
                                        info = result.group(2)
                                        info = hex(int(info))
                                        hex_list.append(data + reg)
                                        hex_list.append(info[2:])
                            sucesso = True
                            break
                        number += 1
            if data: #check the existance of the .data section
                coincideWord = re.search(reg_word, line)
                
                if coincideWord:
                    info = coincideWord.group(1)
                    if info.startswith("0x"):  #deals the data input variation, with or without "0x"
                        hex_list.append(info[2:]) 
                    else:
                        info = int(info)
                        info = hex(info)
                        hex_list.append(info[2:])      
            if halt:  
                coincideHalt = re.search(reg_halt, line)
                if coincideHalt:
                    hex_list.append("40")      
                    total = len(hex_list) - 1
                    total = str(total)
                    total = hex(int(total))
                    hex_list.append(total[2:])
            if move: 
                coincideMove = re.search(reg_move, line)
                if coincideMove:
                    regA = int(coincideMove.group(1))
                    regB = int(coincideMove.group(2))
                    
                    dictReg = {
                        0:"00",
                        1:"01",
                        2:"10",
                        3:"11"
                    }
                    
                    #first XOR
                    regA_op = ''
                    regB_op = ''
                    res = ''

                    for i in dictReg.items():
                        if i[0] == regB:
                            regB_op = '0b' + i[1]
                            regB_op = regB_op + i[1]
                    resF = hex(int(regB_op,2))[2:]
                    hex_list.append('e' + resF)      
                            
                    #add operation 
                    regB_op = ''
                    for i in dictReg.items():
                        if i[0] == regB:
                            regB_op = regB_op + i[1]
                        if i[0] == regA:
                            regA_op = regA_op + i[1]    

                    res = '0b'+regA_op+regB_op
                    resF = hex(int(res,2))[2:]
                    hex_list.append('8' + resF)

                    #second XOR
                    regA_op = ''
                    for i in dictReg.items():
                        if i[0] == regA:
                            regA_op = '0b' + i[1]
                            regA_op = regA_op + i[1]
                    resF = hex(int(regA_op,2))[2:]
                    hex_list.append('e' + resF)  
                    
                
        arquivo.close()
    
    return hex_list

def write_outputfile(memory_file, hex_list):
    #fills the file with "0"
    for i in range(256 - len(hex_list)):
        hex_list.append("0")

    #criation and writing of the hex file
    with open(memory_file, "w") as file:

        line = "v3.0 hex words plain\n"
        file.write(line)
        
        n = 0
        k = 0
        for i in range(0, 16):
            for j in range(0, 16):
                file.write(hex_list[k].zfill(2))
                file.write(' ')
                k+= 1
            n += 16
            file.write("\n")
        file.close()

def main(memory_file, assembly_file):
    hex_list = read_inputfile(assembly_file)
    write_outputfile(memory_file, hex_list)

if (__name__ == '__main__'):
    n = len(sys.argv)
    assert n == 3,'number arguments error'
    main(sys.argv[1], sys.argv[2]) 

