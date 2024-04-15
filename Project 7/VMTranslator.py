import sys

vm_file_name = sys.argv[1]
vm_file = open(vm_file_name, 'r')

base_name = vm_file_name.split('.')[0]
asm_file_name = base_name + '.asm'

asm_file = open(asm_file_name, 'w')

def add():
    asm_file.write("@SP" + "\n")
    asm_file.write("AM=M-1" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("A=A-1" + "\n")
    asm_file.write("M=D+M" + "\n")

def sub():
    asm_file.write("@SP" + "\n")
    asm_file.write("AM=M-1" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("A=A-1" + "\n")
    asm_file.write("M=M-D" + "\n")

def neg():
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M-1" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("M=-D" + "\n")

def eq(eq_counter, end_counter):
    asm_file.write("@SP" + "\n")
    asm_file.write("AM=M-1" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("A=A-1" + "\n")
    asm_file.write("D=M-D" + "\n")
    asm_file.write(f"@EQ{eq_counter}" + "\n")
    asm_file.write("D;JEQ" + "\n")
    asm_file.write("@0" + "\n")
    asm_file.write("D=A" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M-1" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write(f"@END{end_counter}" + "\n")
    asm_file.write("0;JMP" + "\n")
    asm_file.write(f"(EQ{eq_counter})" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M-1" + "\n")
    asm_file.write("M=-1" + "\n")
    asm_file.write(f"(END{end_counter})" + "\n")

def gt(gt_counter, end_counter):
    asm_file.write("@SP" + "\n")
    asm_file.write("AM=M-1" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("A=A-1" + "\n")
    asm_file.write("D=M-D" + "\n")
    asm_file.write(f"@GT{gt_counter}" + "\n")
    asm_file.write("D;JGT" + "\n")
    asm_file.write("@0" + "\n")
    asm_file.write("D=A" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M-1" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write(f"@END{end_counter}" + "\n")
    asm_file.write("0;JMP" + "\n")
    asm_file.write(f"(GT{gt_counter})" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M-1" + "\n")
    asm_file.write("M=-1" + "\n")
    asm_file.write(f"(END{end_counter})" + "\n")

def lt(lt_counter, end_counter):
    asm_file.write("@SP" + "\n")
    asm_file.write("AM=M-1" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("A=A-1" + "\n")
    asm_file.write("D=M-D" + "\n")
    asm_file.write(f"@LT{lt_counter}" + "\n")
    asm_file.write("D;JLT" + "\n")
    asm_file.write("@0" + "\n")
    asm_file.write("D=A" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M-1" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write(f"@END{end_counter}" + "\n")
    asm_file.write("0;JMP" + "\n")
    asm_file.write(f"(LT{lt_counter})" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M-1" + "\n")
    asm_file.write("M=-1" + "\n")
    asm_file.write(f"(END{end_counter})" + "\n")

def land():
    asm_file.write("@SP" + "\n")
    asm_file.write("AM=M-1" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("A=A-1" + "\n")
    asm_file.write("D=D&M" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M-1" + "\n")
    asm_file.write("M=D" + "\n")

def lor():
    asm_file.write("@SP" + "\n")
    asm_file.write("AM=M-1" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("A=A-1" + "\n")
    asm_file.write("D=D|M" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M-1" + "\n")
    asm_file.write("M=D" + "\n")

def lnot(not_counter, end_counter):
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M-1" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("D=!D" + "\n")
    asm_file.write("M=D" + "\n")



def push(segment, index):
    if segment == "constant":
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("D=A" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("M=M+1" + "\n")
    elif segment == "local":
        asm_file.write("@LCL" + "\n")
        asm_file.write("D=M" + "\n")        
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("A=D+A" + "\n")
        asm_file.write("D=M" + "\n")
        asm_file.write("@SP" + "\n")        
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("M=M+1" + "\n")
    elif segment == "argument":
        asm_file.write("@ARG" + "\n")
        asm_file.write("D=M" + "\n")        
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("A=D+A" + "\n")
        asm_file.write("D=M" + "\n")
        asm_file.write("@SP" + "\n")        
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("M=M+1" + "\n") 
    elif segment == "this":
        asm_file.write("@THIS" + "\n")
        asm_file.write("D=M" + "\n")        
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("A=D+A" + "\n")
        asm_file.write("D=M" + "\n")
        asm_file.write("@SP" + "\n")        
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("M=M+1" + "\n") 
    elif segment == "that":
        asm_file.write("@THAT" + "\n")
        asm_file.write("D=M" + "\n")        
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("A=D+A" + "\n")
        asm_file.write("D=M" + "\n")
        asm_file.write("@SP" + "\n")        
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("M=M+1" + "\n") 
    elif segment == "temp":
        asm_file.write("@5" + "\n")
        asm_file.write("D=A" + "\n")        
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("A=D+A" + "\n")
        asm_file.write("D=M" + "\n")
        asm_file.write("@SP" + "\n")        
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("M=M+1" + "\n") 
    elif segment == "pointer":
        asm_file.write("@3" + "\n")
        asm_file.write("D=A" + "\n")        
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("A=D+A" + "\n")
        asm_file.write("D=M" + "\n")
        asm_file.write("@SP" + "\n")        
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("M=M+1" + "\n") 
    elif segment == "static":
        asm_file.write(f"@static{index}" + "\n")
        asm_file.write("D=M" + "\n")        
        asm_file.write("@SP" + "\n")        
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("M=M+1" + "\n")
    else:
        asm_file.write(f"{segment}, {index}")

def pop(segment, index):
    if segment == "local":
        asm_file.write("@LCL" + "\n")
        asm_file.write("D=M" + "\n")        
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("D=D+A" + "\n")
        asm_file.write("@R13" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("AM=M-1" + "\n")        
        asm_file.write("D=M" + "\n")
        asm_file.write("@R13" + "\n")
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
    elif segment == "argument":
        asm_file.write("@ARG" + "\n")
        asm_file.write("D=M" + "\n")        
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("D=D+A" + "\n")
        asm_file.write("@R13" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("AM=M-1" + "\n")        
        asm_file.write("D=M" + "\n")
        asm_file.write("@R13" + "\n")
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
    elif segment == "this":
        asm_file.write("@THIS" + "\n")
        asm_file.write("D=M" + "\n")        
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("D=D+A" + "\n")
        asm_file.write("@R13" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("AM=M-1" + "\n")        
        asm_file.write("D=M" + "\n")
        asm_file.write("@R13" + "\n")
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
    elif segment == "that":
        asm_file.write("@THAT" + "\n")
        asm_file.write("D=M" + "\n")        
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("D=D+A" + "\n")
        asm_file.write("@R13" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("AM=M-1" + "\n")        
        asm_file.write("D=M" + "\n")
        asm_file.write("@R13" + "\n")
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
    elif segment == "temp":
        asm_file.write("@5" + "\n")
        asm_file.write("D=A" + "\n")        
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("D=D+A" + "\n")
        asm_file.write("@R13" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("AM=M-1" + "\n")        
        asm_file.write("D=M" + "\n")
        asm_file.write("@R13" + "\n")
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
    elif segment == "pointer":
        asm_file.write("@3" + "\n")
        asm_file.write("D=A" + "\n")        
        asm_file.write(f"@{index}" + "\n")
        asm_file.write("D=D+A" + "\n")
        asm_file.write("@R13" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("AM=M-1" + "\n")        
        asm_file.write("D=M" + "\n")
        asm_file.write("@R13" + "\n")
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
    elif segment == "static":
        asm_file.write("@SP" + "\n")
        asm_file.write("AM=M-1" + "\n")
        asm_file.write("D=M" + "\n")
        asm_file.write(f"@static{index}" + "\n")        
        asm_file.write("M=D" + "\n")
    else:
        asm_file.write(f"{segment}, {index}")

#This converts vm to asm and eliminates comments and blank space
instruction_list = []
current_instruction = 0 # don't think is needed
for line in vm_file:
    line = line.split('//')[0].strip()
    if line != '':
        instruction_list.append(line)
        current_instruction += 1

eq_counter = 0
lt_counter = 0
gt_counter = 0
not_counter = 0
end_counter = 0

for instruction in instruction_list:
    instruction = instruction.split()
    if len(instruction) == 1:
        if instruction[0] == "add":
            add()
        elif instruction[0] == "sub":
            sub()
        elif instruction[0] == "neg":
            neg()
        elif instruction[0] == "eq":
            eq(eq_counter, end_counter)
            eq_counter += 1
            end_counter += 1
        elif instruction[0] == "gt":
            gt(gt_counter, end_counter)
            gt_counter += 1
            end_counter += 1
        elif instruction[0] == "lt":
            lt(lt_counter, end_counter)
            lt_counter += 1
            end_counter += 1
        elif instruction[0] == "and":
            land()
        elif instruction[0] == "or":
            lor()
        elif instruction[0] == "not":
            lnot(not_counter, end_counter)
            not_counter += 1
            end_counter += 1
    else:               #might change this to if len(instruction) == 3
        if instruction[0] == "push":
            push(instruction[1], instruction[2])
        elif instruction[0] == "pop":
            pop(instruction[1], instruction[2])

    

vm_file.close()
asm_file.close()
