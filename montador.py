"""
Autor: Rodrigo Santos Correa
Objetivo: Disciplina de Organização de Computadores
"""
#bibliotecas necessárias

from ast import arguments
import sys
import re

args = sys.argv

#funções auxiliares

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

    # criação das expressões regulares
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

    lista_hexa = []

    # comparar os dados de entrada do arquivo com as expressões
    with open(assembly_file, "r") as arquivo:
        code = False
        data = False
        halt = False
        move = False
        for linha in arquivo:
            linha = linha.strip()
            if not code:
                prog = re.compile(reg_code, re.IGNORECASE) #faz a indiferenciação entre maiúsculas e minúsculas
                result = prog.match(linha)
                if result is not None: #reconhece bloco .code
                    code = True
            if not data:
                prog = re.compile(reg_data, re.IGNORECASE)
                result = prog.match(linha)
                if result is not None: #reconhece bloco .data
                    data = True
            if not halt:
                prog = re.compile(reg_halt, re.IGNORECASE)
                result = prog.match(linha)
                if result is not None: #reconhece palavra Halt
                    halt = True        
            if not move:
                prog = re.compile(reg_move, re.IGNORECASE)
                result = prog.match(linha)
                if result is not None:  #reconhece palavra Move
                    move = True
            if code:
                sucesso = False
                numero = 0
                for expressao in reg_ula: #lê as expressões, tentando encaixá-las em operações da ULA
                    total = reg_start + expressao + reg_geral
                    recomp = re.compile(total, re.IGNORECASE)
                    result = recomp.match(linha)
                    if result is not None:
                        if (numero >= 0 and numero <= 9):
                            match numero:
                                case 0:
                                    ADD = hexOp2("1000", result)
                                    lista_hexa.append(ADD)
                                case 1:
                                    SHR = hexOp2("1001", result)
                                    lista_hexa.append(SHR)
                                case 2:
                                    SHL = hexOp2("1010", result)
                                    lista_hexa.append(SHL)
                                case 3:
                                    NOT = hexOp2("1011", result)
                                    lista_hexa.append(NOT)
                                case 4:
                                    AND = hexOp2("1100", result)
                                    lista_hexa.append(AND)
                                case 5:
                                    OR = hexOp2("1101", result)
                                    lista_hexa.append(OR)
                                case 6:
                                    XOR = hexOp2("1110", result)
                                    lista_hexa.append(XOR)
                                case 7:
                                    CMP = hexOp2("1111", result)
                                    lista_hexa.append(CMP)
                                case 8:
                                    LD = hexOp2("0000", result)
                                    LD = "{:02x}".format(int(LD, 16))
                                    lista_hexa.append(LD)
                                case 9:
                                    ST = hexOp2("0001", result)
                                    lista_hexa.append(ST)
                        sucesso = True
                        break
                    numero += 1
                if (not sucesso):    #para tratar de operações que não nescessitam da ULA
                    for expressao in reg_not_ula:
                        ex = reg_start + expressao + reg_comment
                        recomp = re.compile(ex, re.IGNORECASE)
                        result = recomp.match(linha)
                        if result is not None:
                            if (numero > 9 and numero <=19):
                                match numero:
                                    case 10:
                                        hexa = result.group(2)
                                        DATA = hexOp1("001000", result, 1)
                                        lista_hexa.append(DATA)
                                        lista_hexa.append(hexa)
                                    case 11:
                                        OUT = hexOp1("011111", result, 1)
                                        lista_hexa.append(OUT)
                                    case 12:
                                        OUT = hexOp1("011110", result, 1)
                                        lista_hexa.append(OUT)
                                    case 13:
                                        IN = hexOp1("011101", result, 1)
                                        lista_hexa.append(IN)
                                    case 14:
                                        IN = hexOp1("011100", result, 1)
                                        lista_hexa.append(IN)
                                    case 15:
                                        CLF = "60"
                                        lista_hexa.append(CLF)
                                    case 16:
                                        JMP = "40"
                                        FLAG = result.group(1)
                                        if (FLAG in lista_hexa) :
                                            LOOP = int(lista_hexa.index(FLAG))
                                            lista_hexa.pop(LOOP)
                                            LOOP = hex(LOOP)[2:].zfill(2)
                                            
                                            lista_hexa.append(JMP)
                                            lista_hexa.append(LOOP)
                                        else:
                                            lista_hexa.append(JMP)
                                            if(FLAG.startswith("0x")):
                                                lista_hexa.append(FLAG[2:])
                                            else:
                                                FLAG = int(FLAG)
                                                FLAG = hex(FLAG)
                                                lista_hexa.append(FLAG[2:])
                                    case 17:
                                        JCAEZ = "0101"
                                        FLAGS = "1" if result.group(1) != "" else "0"
                                        FLAGS = FLAGS + "1" if result.group(2) != "" else FLAGS + "0"
                                        FLAGS = FLAGS + "1" if result.group(3) != "" else FLAGS + "0"
                                        FLAGS = FLAGS + "1" if result.group(4) != "" else FLAGS + "0"
                                        JCAEZ = JCAEZ + FLAGS
                                        JCAEZ = hex(int(JCAEZ,2))[2:]
                                        FLAG = result.group(5)
                                        if (FLAG in lista_hexa) :
                                            LOOP = int(lista_hexa.index(FLAG))
                                            lista_hexa.pop(LOOP)
                                            LOOP = hex(LOOP)[2:].zfill(2)
                                            lista_hexa.append(JCAEZ)
                                            lista_hexa.append(LOOP)
                                        else:
                                            lista_hexa.append(JCAEZ)
                                            if(FLAG.startswith("0x")):
                                                FLAG = FLAG[2:]
                                                lista_hexa.append(FLAG)
                                            else:
                                                FLAG = hex(int(FLAG))
                                                lista_hexa.append(FLAG[2:])
                                    case 18:
                                        FLAG = result.group(1)
                                        FLAG = '3' + FLAG
                                        lista_hexa.append(FLAG)
                                    case 19:
                                        data = '2'
                                        reg = result.group(1)
                                        valor = result.group(2)
                                        valor = hex(int(valor))
                                        lista_hexa.append(data + reg)
                                        lista_hexa.append(valor[2:])
                            sucesso = True
                            break
                        numero += 1
            if data: #trata da palavra "data" usada para colocar dados na memória RAM
                coincideWord = re.search(reg_word, linha)
                
                if coincideWord:
                    valor = coincideWord.group(1)
                    if valor.startswith("0x"):  #trata variação de input, com ou sem o "0x"
                        lista_hexa.append(valor[2:]) 
                    else:
                        valor = int(valor)
                        valor = hex(valor)
                        lista_hexa.append(valor[2:])      
            if halt:  #trata da palavra halt, que simboliza um jump para a mesma linha, criando um loop
                coincideHalt = re.search(reg_halt, linha)
                if coincideHalt:
                    lista_hexa.append("40")      
                    total = len(lista_hexa) - 1
                    total = str(total)
                    total = hex(int(total))
                    lista_hexa.append(total[2:])
            if move: #trata da instrução move, que move o dado de um registrador para outro, apagando os dados anteriores do reg de origem e fim
                coincideMove = re.search(reg_move, linha)
                if coincideMove:
                    regA = int(coincideMove.group(1))
                    regB = int(coincideMove.group(2))
                    
                    dictReg = {
                        0:"00",
                        1:"01",
                        2:"10",
                        3:"11"
                    }
                    
                    #primeiro XOR
                    regA_op = ''
                    regB_op = ''
                    res = ''

                    for i in dictReg.items():
                        if i[0] == regB:
                            regB_op = '0b' + i[1]
                            regB_op = regB_op + i[1]
                    resF = hex(int(regB_op,2))[2:]
                    lista_hexa.append('e' + resF)      
                            
                    #add 
                    regB_op = ''
                    for i in dictReg.items():
                        if i[0] == regB:
                            regB_op = regB_op + i[1]
                        if i[0] == regA:
                            regA_op = regA_op + i[1]    

                    res = '0b'+regA_op+regB_op
                    resF = hex(int(res,2))[2:]
                    lista_hexa.append('8' + resF)
                    #segundo XOR
                    regA_op = ''
                    for i in dictReg.items():
                        if i[0] == regA:
                            regA_op = '0b' + i[1]
                            regA_op = regA_op + i[1]
                    resF = hex(int(regA_op,2))[2:]
                    lista_hexa.append('e' + resF)  
                    
                
        arquivo.close()
    
    return lista_hexa

def write_outputfile(memory_file, lista_hexa):
    #preenche a lista para passar para o arquivo
    for i in range(256 - len(lista_hexa)):
        lista_hexa.append("0")

    #criação e escrita do arquivo hex
    with open(memory_file, "w") as file:

        line = "v3.0 hex words plain\n"
        file.write(line)
        
        n = 0
        k = 0
        for i in range(0, 16):
            for j in range(0, 16):
                file.write(lista_hexa[k].zfill(2))
                file.write(' ')
                k+= 1
            n += 16
            file.write("\n")
        file.close()

def main(memory_file, assembly_file):
    lista_hexa = read_inputfile(assembly_file)
    write_outputfile(memory_file, lista_hexa)

if (__name__ == '__main__'):
    n = len(sys.argv)
    assert n == 3,'number arguments error'
    main(sys.argv[1], sys.argv[2]) 

