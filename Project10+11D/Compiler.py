from Tokenizer import *
from VMWriter import *
from SymbolTable import *
import sys

CONSTANT, ARGUMENT, LOCAL, THIS, THAT, POINTER, STATIC, TEMP = range(8)

INT = 0
KEYWORD = 1
IDENTIFIER = 2
SYMBOL = 3
STR = 4

jack_keywords = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", 
                 "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]

operators = ["+", "-", "*", "/", "&", "|", "<", ">", "=", "-", "~"]

class Compiler:
  def __init__(self, input_file_name, output_file_name):
    self.tokenizer = Tokenizer(input_file_name, jack_keywords)
    self.writer = VMWriter(output_file_name)
    self.symtable = SymbolTable()
    self.num_ifs_called = 0
    self.num_whiles_called = 0
    self.class_name = ""
    
  def expect(self, expected_token):
    token = self.tokenizer.next()
    if not ((token.token_type == SYMBOL or token.token_type == KEYWORD) and token.value == expected_token):
      print(f"Error! Expected {expected_token} but got {token.value}")
      sys.exit(1)

  def compile_class(self):
    self.expect("class")
    self.class_name = self.tokenizer.next().value
    self.expect("{")

    # If peek = "static" or "field" keep compling classVarDec
    while self.tokenizer.peek().value == "static" or self.tokenizer.peek().value == "field":
      self.compileClassVarDec()

    while self.tokenizer.peek().value != "}":
       self.compile_subroutine_dec()
    
    self.expect("}")

  def compileClassVarDec(self):
    # ("static" | "field") type varName (',', varName)* ";"
    kind = self.tokenizer.next().value
    var_type = self.tokenizer.next().value
    varName = self.tokenizer.next().value
    if kind == "static":
      self.symtable.add_global(varName, var_type, STATIC)
    elif kind == "field":
      self.symtable.add_global(varName, var_type, THIS)
    else:
      print(f"expected field or static but got {kind}")
      sys.exit(1)
    while self.tokenizer.peek().value == ",":
      self.expect(',')
      var_name = self.tokenizer.next().value
      if kind == "static":
        self.symtable.add_global(var_name, var_type, STATIC)
      elif kind == "field":
        self.symtable.add_global(var_name, var_type, THIS)
      else:
        print(f"expected field or static but got {kind}")
        sys.exit(1)
    self.expect(";")

  def compile_subroutine_dec(self):
    # ('constructor' | 'function' | 'method')
    self.symtable.reset() #reset the local and arg dicts to be empty
    subroutine_type = self.tokenizer.next().value
    if subroutine_type == "method":
      self.symtable.add_local("Placeholder", int, ARGUMENT) #Dummy entry has to be added before compiling var decs

    return_type = self.tokenizer.next()

    subroutine_name = self.tokenizer.next().value

    self.expect("(")
    if self.tokenizer.peek().value != ")":
      self.compile_ParameterList()
    self.expect(")")

    self.compile_subroutine_body(subroutine_name, subroutine_type)

  def compile_ParameterList(self):
    var_type = self.tokenizer.next().value
    var_name = self.tokenizer.next().value
    self.symtable.add_local(var_name, var_type, ARGUMENT)
    if self.tokenizer.peek().value == ",":
      self.expect(",")
      self.compile_ParameterList()


  def compile_subroutine_body(self, subroutine_name, subroutine_type):
    # '{' varDec* statements '}'
    self.expect("{")

    self.compile_varDecs()
    num_var = self.symtable.get_local_vars()
    self.writer.write_function(self.class_name + "." + subroutine_name, num_var)
  
    if subroutine_type == "constructor":
      num_fields = self.symtable.get_field_vars()
      self.writer.write_push(CONSTANT, num_fields)
      self.writer.write_call("Memory.alloc", 1)
      self.writer.write_pop(POINTER, 0)
    elif subroutine_type == 'method':
      self.writer.write_push(ARGUMENT, 0)
      self.writer.write_pop(POINTER, 0)

    self.compile_Statements() 
    self.expect("}")

  def compile_varDecs(self):
    while self.tokenizer.peek().value == "var":
      self.compile_varDec()

  def compile_varDec(self):
    # 'var' type varName (',' varName)* ';'
    self.expect('var')
    var_type = self.tokenizer.next().value
    var_name = self.tokenizer.next().value
    self.symtable.add_local(var_name, var_type, LOCAL)

    while self.tokenizer.peek().value == ",":
      self.expect(',')
      var_name = self.tokenizer.next().value
      self.symtable.add_local(var_name, var_type, LOCAL)
      
    self.expect(";")

  def compile_Statements(self):
    # letStatment | ifStatement | whileStatement | doStatement | returnStatement
    while self.tokenizer.peek().value in ['let', 'do', 'if', 'while', 'return']:
      next_token = self.tokenizer.peek()
      if next_token.value == "do":
        self.compile_Do()
      elif next_token.value == "return":
        self.compile_Return()
      elif next_token.value == "let":
        self.compile_let()
      elif next_token.value == "if":
        self.compile_if()
      elif next_token.value == "while":
        self.compile_while()

  def compile_let(self):
    is_array = False
    self.expect("let")
    var_name = self.tokenizer.next().value
    if self.tokenizer.peek().value == "[":
      self.compile_Expression()
      if var_name in self.symtable.local_dict.keys():
        self.writer.write_push(self.symtable.local_dict[var_name][1], self.symtable.local_dict[var_name][2])
      elif var_name in self.symtable.global_dict.keys():
        self.writer.write_push(self.symtable.global_dict[var_name][1], self.symtable.global_dict[var_name][2])
      else:
        print(f"expected to be in symbol table but got var_name {var_name}")
        sys.exit(1)
      self.writer.write_raw("add")
      is_array = True
    self.expect("=")
    while self.tokenizer.peek().value != ";":
      self.compile_Expression()
    self.expect(";")
    if is_array:
      self.writer.write_pop(TEMP, 0)
      self.writer.write_pop(POINTER, 1)
      self.writer.write_push(TEMP, 0)
      self.writer.write_pop(THAT, 0)
    else:
      if var_name in self.symtable.local_dict.keys():
        self.writer.write_pop(self.symtable.local_dict[var_name][1], self.symtable.local_dict[var_name][2])
      elif var_name in self.symtable.global_dict.keys():
        self.writer.write_pop(self.symtable.global_dict[var_name][1], self.symtable.global_dict[var_name][2])
      else:
        print(f"expected to be in symbol table but got var_name {var_name}")
        sys.exit(1)

  def compile_if(self):
    # 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}'?)
    self.expect("if")
    self.expect('(')
    while self.tokenizer.peek().value != "{": 
      self.compile_Expression()
    #a self.expect(")") is not needed here because it is skipped by the while loop

    num_if = self.num_ifs_called #to temp hold the number to put on labels
    self.num_ifs_called += 1
    self.writer.write_if("IF_TRUE", num_if)
    self.writer.write_goto("IF_FALSE", num_if)
    self.writer.write_label("IF_TRUE", num_if)

    self.expect("{")
    self.compile_Statements()
    self.expect("}")

    self.writer.write_goto("IF_END", num_if)
    self.writer.write_label("IF_FALSE", num_if)

    if self.tokenizer.peek().value == "else":
      self.expect('else')
      self.expect("{")
      self.compile_Statements()
      self.expect("}")

    self.writer.write_label("IF_END", num_if)

  def compile_while(self):
    # 'while' '(' expression ')' '{' statements '}'

    num_while = self.num_whiles_called #to temp hold the number to put on labels
    self.num_whiles_called += 1
    self.writer.write_label("WHILE_EXP", num_while)

    self.expect("while")
    self.expect("(")
    while self.tokenizer.peek().value != "{":
      self.compile_Expression()
    #a self.expect(")") is not needed here because it is skipped by the while loop

    self.writer.write_raw("not")
    self.writer.write_if("WHILE_END", num_while)

    self.expect("{")
    self.compile_Statements()
    self.expect("}")

    self.writer.write_goto("WHILE_EXP", num_while)
    self.writer.write_label("WHILE_END", num_while)

  def compile_Do(self):
    # 'do' subroutineCall ';'
    self.expect("do")
    self.compile_Expression()
    self.writer.write_pop(TEMP, 0)
    self.expect(";")

  def compile_Return(self):
    # 'return' expression? ';'
    self.expect("return")
    if self.tokenizer.peek().value == ";":
      self.expect(";")
      self.writer.write_push(CONSTANT, 0)
      self.writer.write_Return()
    else:
      while self.tokenizer.peek().value != ";":
        self.compile_Expression()
      self.writer.write_Return()
      self.expect(";")

  def compile_Expression(self):
    # term (op term)*
    peek = self.tokenizer.peek()
    if peek.value == "+":
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("add")
    elif peek.value == "*":
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_call("Math.multiply", 2)
    elif peek.value == "/":
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_call("Math.divide", 2)
    elif peek.value == "-":
      if self.tokenizer.past().value == "(" or self.tokenizer.past().value == "=":
        self.tokenizer.next()
        if self.tokenizer.peek().value == "(":
          self.compile_Expression_List()
        else:
          self.compile_Term()
        self.writer.write_raw("neg")
      else:
        self.tokenizer.next()
        if self.tokenizer.peek().value == "(":
          self.compile_Expression_List()
        else:
          self.compile_Term()
        self.writer.write_raw("sub")
    elif peek.value == "&lt;":
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("lt")
    elif peek.value == "&gt;":
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("gt")
    elif peek.value == "~":
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("not")
    elif peek.value == "=":
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("eq")
    elif peek.value == "&amp;":
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("and")
    elif peek.value == "this":
      self.tokenizer.next()
      self.writer.write_push(POINTER, 0)
    elif peek.value == "|":
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("or")
    else:
      self.compile_Term()

  def compile_Term(self):
    # intConst | stringConstant | keywordConstant | varName | varName '[' expression ']' | '(' expression ')' | unaryOp term | subroutineCall
    token = self.tokenizer.next()
    if self.tokenizer.peek().value == "(" and token.token_type == IDENTIFIER: #if current token is and identifier and next token is ( then must be a function call
      self.writer.write_push(POINTER, 0)
      num_args = self.compile_Expression_List()
      self.writer.write_call(self.class_name + "." + token.value, num_args + 1)
    elif self.tokenizer.peek().value == ".": #if next token is . then must be a __.__ function call
      if token.value in self.symtable.global_dict.keys():
        self.writer.write_push(self.symtable.global_dict[token.value][1], self.symtable.global_dict[token.value][2])
        function_name = self.symtable.global_dict[token.value][0] + self.tokenizer.next().value + self.tokenizer.next().value
        num_args = self.compile_Expression_List()
        self.writer.write_call(function_name, num_args + 1)
      elif token.value in self.symtable.local_dict.keys():
        self.writer.write_push(self.symtable.local_dict[token.value][1], self.symtable.local_dict[token.value][2])
        function_name = self.symtable.local_dict[token.value][0] + self.tokenizer.next().value + self.tokenizer.next().value
        num_args = self.compile_Expression_List()
        self.writer.write_call(function_name, num_args + 1)
      else:
        function_name = token.value + self.tokenizer.next().value + self.tokenizer.next().value
        num_args = self.compile_Expression_List()
        self.writer.write_call(function_name, num_args)
    elif self.tokenizer.peek().value == "[": # means is not setting the value in a let statement (e.g. a do)
      self.expect("[")
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Expression()
      while self.tokenizer.peek().value != "]":
        self.compile_Expression()
      self.expect("]")
      if token.value in self.symtable.local_dict.keys():
        self.writer.write_push(self.symtable.local_dict[token.value][1], self.symtable.local_dict[token.value][2])
      elif token.value in self.symtable.global_dict.keys():
        self.writer.write_push(self.symtable.global_dict[token.value][1], self.symtable.global_dict[token.value][2])
      else:
        print(f"expected to be in symbol table but got var_name {token.value}")
        sys.exit(1)
      self.writer.write_raw('add')
      self.writer.write_pop(POINTER, 1)
      self.writer.write_push(THAT, 0)
    elif token.value == "[": # means came from let statement (needs to be set)
      self.compile_Expression()
      self.expect("]")
    elif token.value == "null":
      self.writer.write_push(CONSTANT, 0)
    elif token.token_type == INT:
      self.writer.write_push(CONSTANT, token.value)
    elif token.value == "true":
      self.writer.write_push(CONSTANT, 0)
      self.writer.write_raw("not")
    elif token.value == "false":
      self.writer.write_push(CONSTANT, 0)
    elif token.token_type == STR:
      self.writer.write_String(token.value)
    elif token.value in self.symtable.local_dict.keys():
      self.writer.write_push(self.symtable.local_dict[token.value][1], self.symtable.local_dict[token.value][2])
    elif token.value in self.symtable.global_dict.keys():
      self.writer.write_push(self.symtable.global_dict[token.value][1], self.symtable.global_dict[token.value][2])


  def compile_Expression_List(self) -> int:
    self.expect("(")
    num_args = 0
    if self.tokenizer.peek().value == "(":
      self.compile_Expression_List()
      num_args += 1
    while self.tokenizer.peek().value != ")":
      if self.tokenizer.peek().value == "(":
        num_args += 1
        self.compile_Expression_List()
      if self.tokenizer.peek().value not in operators and self.tokenizer.peek().value != ",":
        num_args += 1
      self.compile_Expression() 
    self.expect(")")
    return num_args