import sys

asm_file_name = sys.argv[1]
asm_file = open(asm_file_name, 'r')

base_name = asm_file_name.split('.')[0]
hack_file_name = base_name + '.hack'

hack_file = open(hack_file_name, 'w')

symbol_table = {
    "R0": "0",
    "R1": "1",
    "R2": "2",
    "R3": "3",
    "R4": "4",
    "R5": "5",
    "R6": "6",
    "R7": "7",
    "R8": "8",
    "R9": "9",
    "R10": "10",
    "R11": "11",
    "R12": "12",
    "R13": "13",
    "R14": "14",
    "R15": "15",
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4",
    "SCREEN": "16384",
    "KBD": "24576"
}
#Be careful because a = 1 when M is being used in the ALU
alu_instructions = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "A": "110000",
    "M": "110000",    
    "!D": "001101",
    "!A": "110001",
    "!M": "110001",
    "-D": "001111",
    "-A": "110011",
    "-M": "110011",
    "D+1": "011111",
    "A+1": "110111",
    "M+1": "110111",
    "D-1": "001110",
    "A-1": "110010",
    "M-1": "110010",
    "D+A": "000010",
    "D+M": "000010",
    "D-A": "010011",
    "D-M": "010011",
    "A-D": "000111",
    "M-D": "000111",
    "D&A": "000000",
    "D&M": "000000",
    "D|A": "010101",
    "D|M": "010101",     
}

dest_instructions = {
    "M": "001",
    "D": "010",
    "DM": "011",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "MA": "101",
    "AD": "110",
    "DA": "110",
    "ADM": "111"
}

jump_instructions = {
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}
#Eventually add symbol table on first pass
instruction_list = []
current_instruction = 0
for line in asm_file:
    line = line.split('//')[0].strip()
    if line != '':
        if line[0] == '(':
            symbol_table[line[1:-1]] = current_instruction
        else:
            instruction_list.append(line)
            current_instruction += 1

next_available_memory = 16
for instruction in instruction_list:
    if instruction[0] == "@" and instruction[1:].isdigit() == False:
        if instruction[1:] not in symbol_table:
            symbol_table[instruction[1:]] = str(next_available_memory)
            next_available_memory += 1

for instruction in instruction_list:
    if instruction[0] == "@":
        if instruction[1:].isdigit():
            n = int(instruction[1:])
        else:
            n = int(symbol_table[instruction[1:]])
        hack_file.write(f'{n:016b}\n')
    else:
        dest_value = "000"
        alu_value = "000000"
        jump_value = "000"
        a = "0"
        if "=" in instruction:
            index = instruction.index("=")
            dest_value = dest_instructions[instruction[0:index]] ### might need to be more than just the value at 0
            if "M" in instruction[2:]:
                a = "1"
            alu_value = alu_instructions[instruction[index + 1:]] ### Might need to be more than the 2
            #This is where things equal each other (are set to the right side)
        else:
            ###### Check if M is involved to change a
            alu_value = alu_instructions[instruction[0]] #This might need to be changed from inst[0]
            if "M" in instruction[0]:
                a = "1"
            jump_value = jump_instructions[instruction[2:]] #This might need to be different than inst[2:]
            # I think the only else is if there is a jump because of a semicolon

        #this will be where c instructions are converted into the correct binary
        hack_file.write("111" + a + alu_value + dest_value + jump_value + '\n')

asm_file.close()
hack_file.close()
