from Compiler import *
import sys
import os

def compile_file(file):
    vm_file_name = file.split('.')[0] + '.vm'
    compiler = Compiler(file, vm_file_name)
    compiler.compile_class()

def main():
    input = sys.argv[1]
    if os.path.isdir(input):
        for file in os.listdir(input):
            if ".jack" in file:
                compile_file(os.path.join(input, file))
    else:
        compile_file(input)


main()