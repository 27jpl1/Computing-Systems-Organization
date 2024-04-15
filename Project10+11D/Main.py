from Compiler import *
import sys

def main():
    jack_file_name = sys.argv[1]
    vm_file_name = jack_file_name.split('.')[0] + 'vm'
    compiler = Compiler(jack_file_name, vm_file_name)
    compiler.compile_class()


main()