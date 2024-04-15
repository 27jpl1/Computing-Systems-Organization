import os
import sys

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

def lnot():
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M-1" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("D=!D" + "\n")
    asm_file.write("M=D" + "\n")

def push(function_name, segment, index):
    function_name = function_name.split(".")[0]
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
        asm_file.write(f"@{function_name}{index}" + "\n")
        asm_file.write("D=M" + "\n")        
        asm_file.write("@SP" + "\n")        
        asm_file.write("A=M" + "\n")
        asm_file.write("M=D" + "\n")
        asm_file.write("@SP" + "\n")
        asm_file.write("M=M+1" + "\n")
    else:
        asm_file.write(f"{segment}, {index}")

def pop(function_name, segment, index):
    function_name = function_name.split(".")[0]
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
        asm_file.write(f"@{function_name}{index}" + "\n")        
        asm_file.write("M=D" + "\n")
    else:
        asm_file.write(f"{segment}, {index}")

def label(base_name, label):
    asm_file.write(f"({base_name}${label})" + "\n")

def goto(base_name, name):
    asm_file.write(f"@{base_name}${name}" + "\n")
    asm_file.write("0;JMP" + "\n")

def ifgoto(base_name, name):
    asm_file.write("@SP" + "\n")
    asm_file.write("AM=M-1" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write(f"@{base_name}${name}" + "\n")
    asm_file.write("D;JNE" + "\n")        

def new_function(name, n_var):
    global current_function
    current_function = name
    asm_file.write(f"({name})" + "\n")
    i = 0
    while i < int(n_var):
        push(current_function, "constant", 0)
        i += 1

def function_return():
    asm_file.write("@LCL" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("@R13" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write("D=M" + "\n")        
    asm_file.write("@5" + "\n")
    asm_file.write("A=D-A" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("@R14" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M-1" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("@ARG" + "\n")        
    asm_file.write("A=M" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write("@ARG" + "\n")
    asm_file.write("D=M" + "\n")   
    asm_file.write("@SP" + "\n")
    asm_file.write("M=D+1" + "\n")
    asm_file.write("@R13" + "\n")
    asm_file.write("A=M-1" + "\n")  
    asm_file.write("D=M" + "\n")  
    asm_file.write("@THAT" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write("@R13" + "\n")
    asm_file.write("D=M" + "\n")        
    asm_file.write("@2" + "\n")
    asm_file.write("A=D-A" + "\n")
    asm_file.write("D=M" + "\n") 
    asm_file.write("@THIS" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write("@R13" + "\n")
    asm_file.write("D=M" + "\n")        
    asm_file.write("@3" + "\n")
    asm_file.write("A=D-A" + "\n")
    asm_file.write("D=M" + "\n") 
    asm_file.write("@ARG" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write("@R13" + "\n")
    asm_file.write("D=M" + "\n")        
    asm_file.write("@4" + "\n")
    asm_file.write("A=D-A" + "\n")
    asm_file.write("D=M" + "\n") 
    asm_file.write("@LCL" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write("@R14" + "\n")
    asm_file.write("A=M" + "\n") 
    asm_file.write("0;JMP" + "\n")  

def call(name, m, return_counter):
    asm_file.write(f"@return{return_counter}" + "\n")
    asm_file.write("D=A" + "\n")        
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("M=M+1" + "\n")
    asm_file.write("@LCL" + "\n")
    asm_file.write("D=M" + "\n")        
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("M=M+1" + "\n")
    asm_file.write("@ARG" + "\n")
    asm_file.write("D=M" + "\n")        
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("M=M+1" + "\n")
    asm_file.write("@THIS" + "\n")
    asm_file.write("D=M" + "\n")        
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("M=M+1" + "\n")
    asm_file.write("@THAT" + "\n")
    asm_file.write("D=M" + "\n")        
    asm_file.write("@SP" + "\n")
    asm_file.write("A=M" + "\n")
    asm_file.write("M=D" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("M=M+1" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("D=M" + "\n")
    asm_file.write("@LCL" + "\n")
    asm_file.write("M=D" + "\n")  
    n = 5 + int(m)
    asm_file.write(f"@{n}" + "\n")
    asm_file.write("D=A" + "\n")
    asm_file.write("@SP" + "\n")
    asm_file.write("D=M-D" + "\n")  
    asm_file.write("@ARG" + "\n")
    asm_file.write("M=D" + "\n")

    asm_file.write(f"@{name}" + "\n")
    asm_file.write("0;JMP" + "\n")  
    asm_file.write(f"(return{return_counter})" + "\n")  

eq_counter = 0
lt_counter = 0
gt_counter = 0
end_counter = 0
return_counter = 1
current_function = "Sys.init"

def translate_vm(vm_file_name):
    global eq_counter
    global lt_counter
    global gt_counter
    global end_counter
    global return_counter
    global current_function

    vm_file = open(vm_file_name, 'r')
    vm_file_name = vm_file_name.replace("/", "")
    instruction_list = []
    current_instruction = 0 # don't think is needed
    for line in vm_file:
        line = line.split('//')[0].strip()
        if line != '':
            instruction_list.append(line)
            current_instruction += 1

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
                lnot()
            elif instruction[0] == "return":
                function_return()
        else:               #might change this to if len(instruction) == 3
            if instruction[0] == "push":
                push(current_function, instruction[1], instruction[2])
            elif instruction[0] == "pop":
                pop(current_function, instruction[1], instruction[2])
            elif instruction[0] == "label":
                label(current_function, instruction[1])
            elif instruction[0] == "goto":
                goto(current_function, instruction[1])
            elif instruction[0] == "if-goto":
                ifgoto(current_function, instruction[1])
            elif instruction[0] == "function":
                new_function(instruction[1], instruction[2])
            elif instruction[0] == "call":
                call(instruction[1], instruction[2], return_counter)
                return_counter += 1

def generate_bootstrap(vm_file_name):
    asm_file.write("@256" + "\n")
    asm_file.write("D=A" + "\n")   
    asm_file.write("@SP" + "\n")
    asm_file.write("M=D" + "\n")
    call("Sys.init", 0, 0)    

vm_file_name = sys.argv[1]

asm_file_name = vm_file_name.split('.')[0] + '.asm'
asm_file = open(asm_file_name, 'w')

generate_bootstrap(vm_file_name)

if os.path.isdir(vm_file_name):
    for f in os.listdir(vm_file_name):
        if ".vm" in f:
            translate_vm(os.path.join(vm_file_name, f))

else:
    translate_vm(vm_file_name)

asm_file.close()
