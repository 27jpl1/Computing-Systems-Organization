CONSTANT, ARGUMENT, LOCAL, THIS, THAT, POINTER, STATIC, TEMP = range(8)

seg_names = {
    CONSTANT: 'constant',
    ARGUMENT: 'argument',
    LOCAL: 'local',
    THIS: 'this',
    THAT: 'that',
    POINTER: 'pointer',
    STATIC: 'static',
    TEMP: 'temp'
}

class VMWriter:
    def __init__(self, output_file_name):
        self.f = open(output_file_name, 'w')

    def write_push(self, seg, index):
        self.f.write(f'push {seg_names[seg]} {index}\n')

    def write_pop(self, seg, index):
        self.f.write(f"pop {seg_names[seg]} {index}\n")

    def write_raw(self, txt):
        self.f.write(txt + '\n')

    #write label
    #write goto
    #write if

    def write_call(self, function_name, num_args):
        self.f.write(f'call {function_name} {num_args}\n')

    def write_function(self, name, vars):
        self.f.write(f"function {name} {vars}\n")

    def write_Return(self):
        self.f.write("return\n")