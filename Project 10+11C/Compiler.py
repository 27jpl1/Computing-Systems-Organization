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
    
  def expect(self, expected_token):
    token = self.tokenizer.next()
    if not ((token.token_type == SYMBOL or token.token_type == KEYWORD) and token.value == expected_token):
      print(f"Error! Expected {expected_token} but got {token.value}")
      sys.exit(1)

  def compile_class(self):
    self.expect("class")
    class_name = self.tokenizer.next().value
    self.expect("{")

    # Do something with classVarDec*

    while self.tokenizer.peek().value != "}":
       self.compile_subroutine_dec(class_name)
    
    self.expect("}")

  # compileClassVarDec

  def compile_subroutine_dec(self, class_name):
    # ('constructor' | 'function' | 'method') but only function for now
    self.symtable.reset() #reset the local and arg dicts to be empty
    subroutine_type = self.tokenizer.next()

    # ('void' | 'type') but only void for now
    return_type = self.tokenizer.next()

    # subroutineName
    subroutine_name = self.tokenizer.next().value

    self.expect("(")
    if self.tokenizer.peek().value != ")":
      self.compile_ParameterList()
    self.expect(")")

    self.compile_subroutine_body(class_name, subroutine_name)

  def compile_ParameterList(self):
    var_type = self.tokenizer.next().value
    var_name = self.tokenizer.next().value
    self.symtable.add_local(var_name, var_type, ARGUMENT)
    if self.tokenizer.peek().value == ",":
      self.expect(",")
      self.compile_ParameterList()


  def compile_subroutine_body(self, class_name, subroutine_name):
    # '{' varDec* statements '}'
    self.expect("{")

    self.compile_varDecs()
    print(self.symtable.local_dict)
    num_var = self.symtable.get_local_vars()
    self.writer.write_function(class_name + "." + subroutine_name, num_var)

    self.compile_Statements()
    print("i compiled statements")
    self.expect("}")

  def compile_varDecs(self):
    #here to compile a list of vars
    #will call compile_varDec to compile a singular var declaration
    while self.tokenizer.peek().value == "var":
      print("i compiled a var")
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
    self.expect("let")
    var_name = self.tokenizer.next().value
    self.expect("=")
    while self.tokenizer.peek().value != ";":
      print(self.tokenizer.peek().value, "peek")
      self.compile_Expression()
    print("i broke")
    self.expect(";")
    #Will probably have to change this for when global variables are introduced
    print(self.symtable.local_dict[var_name][1], self.symtable.local_dict[var_name][2])
    self.writer.write_pop(self.symtable.local_dict[var_name][1], self.symtable.local_dict[var_name][2])

  def compile_if(self):
    # 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}'?)
    self.expect("if")
    self.expect('(')
    while self.tokenizer.peek().value != "{":  #should work because if put ) it would not pay attention to the last term/expression
      print(self.tokenizer.peek().value, "peeked value")
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
      print("in else")
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
    while self.tokenizer.peek().value != "{":  #should work because if put ) it would not pay attention to the last term/expression
      print(self.tokenizer.peek().value, "peeked value")
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
    self.writer.write_pop(TEMP, 0) #I think this only applies when the return value does not matter
    self.expect(";")

  def compile_Return(self):
    # 'return' expression? ';'
    self.expect("return")
    if self.tokenizer.peek().value == ";":
      self.expect(";")
      self.writer.write_push(CONSTANT, 0) #This is because no return value/ignored
      self.writer.write_Return()
    else:
      print("in return")
      while self.tokenizer.peek().value != ";":
        self.compile_Expression()
      print("past compile exp")
      print(self.tokenizer.peek().value)
      self.writer.write_Return()
      self.expect(";")

  def compile_Expression(self):
    # term (op term)*
    #print(token.value)
    peek = self.tokenizer.peek()
    if peek.value == "+":
      self.tokenizer.next()
      print("hit add")
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("add")
      print("wrote add")
    elif peek.value == "*":
      self.tokenizer.next()
      print("hit multiply")
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_call("Math.multiply", 2)
      print("wrote multiply")
    elif peek.value == "-":
      self.tokenizer.next()
      print("got into -")
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("sub")
    elif peek.value == "&lt;":
      print("i see the less than")
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("lt")
    elif peek.value == "&gt;":
      print("i saw gt")
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("gt")
    elif peek.value == "~":   # I think this might need to be in term, but I think it is fine here
      print("made to ~")
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
        print("expression list not")
        print(self.tokenizer.peek().value, "next value")
      else:
        self.compile_Term()
      print("wrote not")
      self.writer.write_raw("not")
    elif peek.value == "=":
      print("made to =")
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("eq")
    elif peek.value == "&amp;":
      print("made to &")
      self.tokenizer.next()
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List()
      else:
        self.compile_Term()
      self.writer.write_raw("and")
    else:
      self.compile_Term()

  def compile_Term(self):
    # intConst | stringConstant | keywordConstant | varName | varName '[' expression ']' | '(' expression ')' | unaryOp term | subroutineCall
    token = self.tokenizer.next()
    print("term", token.value)
    if self.tokenizer.peek().value == "(": #if next token is ( then must be a function call
      num_args = self.compile_Expression_List()
      self.writer.write_call(token.value, num_args)
    elif self.tokenizer.peek().value == ".": #if next token is . then must be a __.__ function call (more specifics later I think)
      function_name = token.value + self.tokenizer.next().value + self.tokenizer.next().value
      num_args = self.compile_Expression_List()
      self.writer.write_call(function_name, num_args)
    elif token.token_type == INT:
      self.writer.write_push(CONSTANT, token.value)
      print("pushed term")
    elif token.value == "true":
      self.writer.write_push(CONSTANT, 0)
      self.writer.write_raw("not")
    elif token.value == "false":
      self.writer.write_push(CONSTANT, 0)
    elif token.value in self.symtable.local_dict: #I think this changes somewhat when class varaibles come into play
      self.writer.write_push(self.symtable.local_dict[token.value][1], self.symtable.local_dict[token.value][2])
    elif token.token_type == STR:
      self.writer.write_String(token.value)

  def compile_Expression_List(self) -> int:
    self.expect("(")
    if self.tokenizer.peek().value == "(":
      self.compile_Expression_List()
    num_args = 0
    while self.tokenizer.peek().value != ")":
      if self.tokenizer.peek().value not in operators and self.tokenizer.peek().value != ",":
        print(self.tokenizer.peek().value, "expression list not")
      #since is not an expression should not count towards number or args
        num_args += 1
      self.compile_Expression() 
    self.expect(")")
    return num_args