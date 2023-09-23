import copy

# CPU out-flags
COO = 0b00_000_001 # Counter-Out Flag
IRO = 0b00_000_010 # Instruction Register-Out Flag
RAO = 0b00_000_011 # RAM-Out Flag
ARO = 0b00_000_100 # A Register-Out Flag
SKP = 0b00_000_101 # B Register-Out Flag
SUO = 0b00_000_110 # Sum-Out Flag
HLT = 0b00_000_111 # Halt Flag

# CPU in-flags
JMP = 0b00_001_000 # Jump Flag
IRI = 0b00_010_000 # Instruction Register-In Flag
RAI = 0b00_011_000 # RAM-In Flag
ARI = 0b00_100_000 # A Register-In Flag
BRI = 0b00_101_000 # B Register-In Flag
MEI = 0b00_110_000 # Memory-In Flag
OUI = 0b00_111_000 # Output-In Flag

# CPU Special-flags
COE = 0b01_000_000 # Counter-enable Flag
SUB = 0b10_000_000 # Subtract Flag

func_Template = [
    [MEI|COO,   RAO|IRI|COE,    SKP,        SKP,            SKP,           SKP, SKP, SKP],     # 0000 - NOP
    [MEI|COO,   RAO|IRI|COE,    IRO|MEI,    RAO|ARI,        SKP,           SKP, SKP, SKP],     # 0001 - LDA
    [MEI|COO,   RAO|IRI|COE,    IRO|MEI,    RAO|BRI,        SUO|ARI,       SKP, SKP, SKP],     # 0010 - ADD
    [MEI|COO,   RAO|IRI|COE,    IRO|MEI,    RAO|BRI,        SUO|ARI|SUB,   SKP, SKP, SKP],     # 0011 - SUB
    [MEI|COO,   RAO|IRI|COE,    IRO|MEI,    ARO|RAI,        SKP,           SKP, SKP, SKP],     # 0100 - STA
    [MEI|COO,   RAO|IRI|COE,    IRO|ARI,    SKP,            SKP,           SKP, SKP, SKP],     # 0101 - LDI
    [MEI|COO,   RAO|IRI|COE,    IRO|JMP,    SKP,            SKP,           SKP, SKP, SKP],     # 0110 - JMP
    [MEI|COO,   RAO|IRI|COE,    SKP,        SKP,            SKP,           SKP, SKP, SKP],     # 0111 - JC
    [MEI|COO,   RAO|IRI|COE,    SKP,        SKP,            SKP,           SKP, SKP, SKP],     # 1000 - JZ
    [MEI|COO,   RAO|IRI|COE,    IRO|BRI,    SUO|ARI,        SKP,           SKP, SKP, SKP],     # 1001 - INC
    [MEI|COO,   RAO|IRI|COE,    IRO|BRI,    SUO|ARI|SUB,    SKP,           SKP, SKP, SKP],     # 1010 - DEC
    [MEI|COO,   RAO|IRI|COE,    SKP,        SKP,            SKP,           SKP, SKP, SKP],     # 1011 - NOP
    [MEI|COO,   RAO|IRI|COE,    SKP,        SKP,            SKP,           SKP, SKP, SKP],     # 1100 - NOP
    [MEI|COO,   RAO|IRI|COE,    SKP,        SKP,            SKP,           SKP, SKP, SKP],     # 1101 - NOP
    [MEI|COO,   RAO|IRI|COE,    ARO|OUI,    SKP,            SKP,           SKP, SKP, SKP],     # 1110 - OUT
    [MEI|COO,   RAO|IRI|COE,    HLT,        SKP,            SKP,           SKP, SKP, SKP]      # 1111 - HLT
]

func_Template_List = [
    func_Template,
    copy.deepcopy(func_Template),
    copy.deepcopy(func_Template),
    copy.deepcopy(func_Template)
]

# Carry bit is 1
func_Template_List[0b01][0b0111][0b10] = IRO|JMP

# Zero bit is 1
func_Template_List[0b10][0b1000][0b10] = IRO|JMP

# Both bits are 1
func_Template_List[0b11][0b0111][0b10] = IRO|JMP
func_Template_List[0b11][0b1000][0b10] = IRO|JMP

with open("Compiled.txt", "w") as file:
    for adress in range(512):
        if adress % 8 == 0 and adress != 0:
            file.write("\n")

        flags = adress >> 7
        instruction = (adress & 0b001111000) >> 3
        step = adress & 0b000000111
        
        write = hex(func_Template_List[flags][instruction][step])
        file.write(write)
        file.write(f"   " + (" " * (6 - len(write))))