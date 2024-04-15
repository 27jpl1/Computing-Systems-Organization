from Tokenizer import *
from VMWriter import *
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
    subroutine_type = self.tokenizer.next()

    # ('void' | 'type') but only void for now
    return_type = self.tokenizer.next()

    # subroutineName
    subroutine_name = self.tokenizer.next().value

    self.expect("(")
    #compileParameterList here, but not for now
    num_params = 0 #will change once compileParameterList is added
    self.expect(")")

    self.writer.write_function(class_name + "." + subroutine_name, num_params)

    self.compile_subroutine_body()

  #compileParameterList

  def compile_subroutine_body(self):
    # '{' varDec* statements '}'
    self.expect("{")

    #deal with VarDec, but not for now

    self.compile_Statements()

    self.expect("}")

  #compileVarDec

  def compile_Statements(self):
    # letStatment | ifStatement | whileStatement | doStatement | returnStatement
    # only doStatement and returnStatement needed for now
    while self.tokenizer.peek().value in ['let', 'do', 'if', 'while', 'return']:
      next_token = self.tokenizer.peek()
      if next_token.value == "do":
         self.compile_Do()
      elif next_token.value == "return":
        self.compile_Return()

  #compileLet

  #compileIf

  #compileWhile

  def compile_Do(self):
    # 'do' subroutineCall ';'
    self.expect("do")
    self.compile_Expression()
    self.expect(";")

  def compile_Return(self):
    # 'return' expression? ';'
    self.expect("return")
    #deal with expressions here, but can ignore for now
    self.expect(";")
    self.writer.write_push(CONSTANT, 0) #think this is because no return value/ignored
    self.writer.write_Return()

  def compile_Expression(self):
    #print(token.value)
    peek = self.tokenizer.peek()
    if peek.value == "+":
      self.tokenizer.next()
      print("hit add")
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List("add")
      else:
        self.compile_Term()
      self.writer.write_raw("add")
      print("wrote add")
    elif peek.value == "*":
      self.tokenizer.next()
      print("hit multiply")
      if self.tokenizer.peek().value == "(":
        self.compile_Expression_List("mult")
      else:
        self.compile_Term()
      self.writer.write_call("Math.multiply", 2)
      print("wrote multiply")
    else:
      self.compile_Term()

  def compile_Term(self):
    token = self.tokenizer.next()
    print("term", token.value)
    if self.tokenizer.peek().value == "(": #if next token is ( then must be a function call
      num_args = self.compile_Expression_List()
      self.writer.write_call(token.value, num_args)
    elif self.tokenizer.peek().value == ".": #if next token is . then must be a __.__ function call
      function_name = token.value + self.tokenizer.next().value + self.tokenizer.next().value
      num_args = self.compile_Expression_List("output")
      self.writer.write_call(function_name, num_args)
      self.writer.write_pop(TEMP, 0) #this is a thing. Do not know why
    elif token.token_type == INT:
      self.writer.write_push(CONSTANT, token.value)
      print("pushed term")
    

  def compile_Expression_List(self, name) -> int:
    self.expect("(")
    num_args = 0
    while self.tokenizer.peek().value != ")":
      print("list", name, self.tokenizer.peek().value)
      if self.tokenizer.peek().value not in operators: #since is not an expression should not count towards number or args
        num_args += 1
      self.compile_Expression() 
    self.expect(")")
    return num_args