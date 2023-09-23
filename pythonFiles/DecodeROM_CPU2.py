import copy

# Control Flags

# Out-Group
PCO = 0b00_000_001 # Counter-Out Flag
IRO = 0b00_000_010 # Instruction Register-Out Flag
RAO = 0b00_000_011 # RAM-Out Flag
ARO = 0b00_000_100 # A Register-Out Flag
SKP = 0b00_000_101 # B Register-Out Flag
ALO = 0b00_000_110 # Sum-Out Flag
HLT = 0b00_000_111 # Halt Flag

# In-Group
JMP = 0b00_001_000 # Jump Flag
IRI = 0b00_010_000 # Instruction Register-In Flag
RAI = 0b00_011_000 # RAM-In Flag
ARI = 0b00_100_000 # A Register-In Flag
BRI = 0b00_101_000 # B Register-In Flag
MRI = 0b00_110_000 # Memory-In Flag
ORI = 0b00_111_000 # Output-In Flag

# Special Case
PCE = 0b01_000_000 # Counter-enable Flag
SUB = 0b10_000_000 # Subtract Flag

# Base functions
func_Template = [
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 00000 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  RAO|ARI|PCE,    SKP,         SKP, SKP, SKP, SKP],     # 00001 - LDA #
    [PCO|MRI,  RAO|IRI|PCE,  RAO|BRI|PCE,    ALO|ARI,     SKP, SKP, SKP, SKP],     # 00010 - ADD #
    [PCO|MRI,  RAO|IRI|PCE,  RAO|BRI|PCE,    ALO|ARI|SUB, SKP, SKP, SKP, SKP],     # 00011 - SUB #
    [PCO|MRI,  RAO|IRI|PCE,  RAO|MRI|PCE,    RAI|ARO,     SKP, SKP, SKP, SKP],     # 00100 - STA #
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 00101 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  RAO|JMP|PCE,    SKP,         SKP, SKP, SKP, SKP],     # 00110 - JMP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 00111 - JC
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 01000 - JZ
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 01001 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 01010 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 01011 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 01100 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 01101 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 01110 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 01111 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 10000 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 10001 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 10010 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 10011 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 10100 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 10101 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 10110 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 10111 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 11000 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 11001 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 11010 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 11011 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 11100 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  SKP,            SKP,         SKP, SKP, SKP, SKP],     # 11101 - NOP
    [PCO|MRI,  RAO|IRI|PCE,  ARO|ORI,        SKP,         SKP, SKP, SKP, SKP],     # 11110 - OUT
    [PCO|MRI,  RAO|IRI|PCE,  HLT,            SKP,         SKP, SKP, SKP, SKP]      # 11111 - HLT
]

# Copies of base functions
func_Template_List = [
    copy.deepcopy(func_Template),
    copy.deepcopy(func_Template),
    copy.deepcopy(func_Template),
    copy.deepcopy(func_Template)
]

# Carry bit is 1
func_Template_List[0b01][0b00111][0b010] = RAO|JMP|PCE

# Zero bit is 1
func_Template_List[0b10][0b01000][0b010] = RAO|JMP|PCE

# Both bits are 1
func_Template_List[0b11][0b00111][0b010] = RAO|JMP|PCE
func_Template_List[0b11][0b01000][0b010] = RAO|JMP|PCE

with open("Compiled.txt", "w") as file:
    for adress in range(2**10):
        if adress % 8 == 0 and adress != 0:
            file.write("\n")

        flags = adress >> 8
        instruction = (adress & 0b0011111000) >> 3
        step = adress & 0b0000000111
        
        write = hex(func_Template_List[flags][instruction][step])
        file.write(write)
        file.write(f"   " + (" " * (6 - len(write))))