# Assembly Converter
This program is an assembly converter system. It reads an assembly file and converts it to a Hex plain file to be used in simulators such as Logisim

# Required imports 
- Regex for regular expressions treatment
- Ast to process trees of python abstract grammar
 
# Usage:
$python converter.py output.mem input.asm

1. The program will only starts to convert once it reads ".code"
2. Use ".data" to start a section of data inputs

See the example in the end for completely understandment

# Reserved Words
- ".code" : starts the coding section
- "data" : starts the data section
- word : input a data in the memory
- halt : loops the program infinitely
- move : move the data from a register to another register, cleaning the old information
  
# The convertable operations are:
Using ALU (Arithmetic Logical Unit):
- Add
- Shr (shift right)
- Shl (shift left)
- Not
- And
- Or 
- Xor
- Cmp (compare)

Not using ALU:
- Ld (load)
- St (store)
- Data
- Out
- In
- Clf (clear all flags)
- Jmp
- Jcaez (jump if C:carry A:a_larger E:equal Z:zero)
- Jmpr 

# Example

Input (assembly file)
```
.code 
    add r0,r1
    shr r0,r1
    shl r0,r1
    not r0,r1
    data r0,15
    data r3,0x05
    and r0,r1
    or r0,r1
    xor r0,r1
    cmp r0,r1
    ld r0,r1
    st r0,r1
    jmpr r3
    jmp 0x20
    ja 0x13
    clf
    in data,r1 
    in addr, r2
    out data, r3
    out addr, r0
    move r1, r0
    halt
.data 
    word 10
    word 0x15
```
Output (memory file)
```
v3.0 hex words plain

81 91 a1 b1 20 0f 23 05 c1 d1 e1 f1 01 11 33 40 
20 54 13 60 71 76 7b 7c e0 84 e5 40 1b 0a 15 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
```
# FAQ 
1. Q: Are the instructions case sensitive?   
A: No, using re.IGNORECASE(), the software can handle any form of input


2. Q: Inputs using decimal form and 0x[number] are the same?

   A: No, it will be converted to hexadecimal value. So if the input is 0x05, when converted it will be 05.
   However, if the input is 5 the output will be 0f, as seen in the example above


3. Q: Does it need the ".data" section to work?

   A: No, it only requires the ".code" section


4. Q:Does it work without identantion?

   A: Yes
