CONSTANT, ARGUMENT, LOCAL, THIS, THAT, POINTER, STATIC, TEMP = range(8)

class SymbolTable:
    def __init__(self):
        self.global_dict = {}
        self.local_dict = {}
        self.local_index = 0
        self.arg_index = 0
        self.static_index = 0
        self.field_index = 0
    
    def reset(self):
        self.local_index = 0
        self.arg_index = 0
        self.local_dict = {}
    
    def add_local(self, var, type, kind):
        if kind == LOCAL:
            self.local_dict[var] = [type, kind, self.local_index]
            self.local_index += 1
        elif kind == ARGUMENT:
            self.local_dict[var] = [type, kind, self.arg_index]
            self.arg_index += 1
        else:
            print("Error!")
    
    def add_global(self, var, type, kind):
        if kind == STATIC:
            self.global_dict[var] = [type, kind, self.static_index]
            self.static_index += 1
        elif kind == THIS:
            self.global_dict[var] = [type, kind, self.field_index]
            self.field_index += 1
        else:
            print("Error!")
    
    def get_local_vars(self) -> int:
        total = 0
        for key in self.local_dict.keys():
            if self.local_dict[key][1] == LOCAL:  #this makes sure only local vars are counted
                total += 1
        return total
    
    # Symbol table - A dictinoary mapping varaible names to information about a variable
    # Need to know the type, kind (local, argument, static, or field), index within its segment (assigned in sequence starting from 0)
    # Symbol table also needs to remember the next available index for each kind
    #2 Symbol tables:
    #Global symbol table for static and field variables
    #Local symbol table for locan and argument variables, which resets to empty at the beginning of each new subroutine

    #can make a method from symbol table to get how many local vars are created