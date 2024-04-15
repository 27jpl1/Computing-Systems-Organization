from Tokenizer import *
import os
import sys

INT = 0
KEYWORD = 1
IDENTIFIER = 2
SYMBOL = 3
STR = 4


jack_keywords = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", 
                 "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]

def main():
    tokenizer = Tokenizer(jack_file_name, jack_keywords)
    txml_file.write("<tokens>" + "\n")
    while tokenizer.has_more_tokens():
        t = tokenizer.next()

        if t.token_type == INT:
            txml_file.write(f"<integerConstant> {t.value} </integerConstant>" + "\n")
        elif t.token_type == KEYWORD:
            txml_file.write(f"<keyword> {t.value} </keyword>" + "\n")
        elif t.token_type == IDENTIFIER:
            txml_file.write(f"<identifier> {t.value} </identifier>" + "\n")
        elif t.token_type == SYMBOL:
            txml_file.write(f"<symbol> {t.value} </symbol>" + "\n")
        elif t.token_type == STR:
            txml_file.write(f"<stringConstant> {t.value} </stringConstant>" + "\n")
    txml_file.write("</tokens>" + "\n")

jack_file_name = sys.argv[1]
jack_file = open(jack_file_name, 'r')

txml_file_name = jack_file_name.split('.')[0] + 'T.xml'
txml_file = open(txml_file_name, 'w')

main()

jack_file.close()
txml_file.close()