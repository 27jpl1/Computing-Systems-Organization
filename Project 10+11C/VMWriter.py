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
        # self.label_table = {} # a dict of labels where the key is the label and the value is the next number to put on end of it
        # self.if_table = {} # a dict of if-goto labels where the key is the label and the value is the next number to put on the end of it
        # self.goto_table = {} # a dict of goto labels where the key is the label an the value is the next number to put on the end of it

    def write_push(self, seg, index):
        self.f.write(f'push {seg_names[seg]} {index}\n')

    def write_pop(self, seg, index):
        self.f.write(f"pop {seg_names[seg]} {index}\n")

    def write_raw(self, txt):
        self.f.write(txt + '\n')

    def write_label(self, label, index):
        self.f.write(f"label {label}{index}" + "\n")
        # if label in self.label_table.keys():
        #     self.f.write(f"label {label}{self.label_table[label]}" + "\n")
        #     self.label_table[label] += 1
        # else:
        #     self.f.write(f"label {label}0" + "\n")
        #     self.label_table[label] = 1
    
    def write_goto(self, label, index):
        self.f.write(f"goto {label}{index}" + "\n")
        # if label in self.goto_table.keys():
        #     self.f.write(f"goto {label}{self.goto_table[label]}" + "\n")
        #     self.goto_table[label] += 1
        # else:
        #     self.f.write(f"goto {label}0" + "\n")
        #     self.goto_table[label] = 1

    def write_if(self, label, index):
        self.f.write(f"if-goto {label}{index}" + "\n")
        # if label in self.if_table.keys():
        #     self.f.write(f"if-goto {label}{self.if_table[label]}" + "\n")
        #     self.if_table[label] += 1
        # else:
        #     self.f.write(f"if-goto {label}0" + "\n")
        #     self.if_table[label] = 1

    def write_call(self, function_name, num_args):
        self.f.write(f'call {function_name} {num_args}\n')

    def write_function(self, name, vars):
        self.f.write(f"function {name} {vars}\n")

    def write_Return(self):
        self.f.write("return\n")
    
    def write_String(self, str):
        self.write_push(CONSTANT, len(str))
        self.write_call("String.new", 1)
        for char in str:
            self.write_push(CONSTANT, ord(char))
            self.write_call("String.appendChar", 2)