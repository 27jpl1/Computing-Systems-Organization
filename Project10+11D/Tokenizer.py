INT = 0
KEYWORD = 1
IDENTIFIER = 2
SYMBOL = 3
STR = 4

def is_ident_char(c):
    return c.isalnum() or c == "_"

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value #Type will depend on the token_type

class Tokenizer:
    def __init__(self, input_file_name, keywords):
        with open(input_file_name) as input_file: # read the entire input file and save it in a variable
            self.text = input_file.read()
        
        self.keywords = keywords
        self.pos = 0 # keep track of our current position in the text

        self.tokens = [] #List of all tokens
        self.cur_token = 0 #Index of the current token

        self.process_tokens()
    
    #Read all the tokens into a list
    def process_tokens(self):
        self.eat_whitespace()

        while self.pos < len(self.text):
            self.tokens.append(self.advance())

    # By convention we will always call this function right after reading in each toekn, so we will be ready to read the next token
    def eat_whitespace(self):   #Skip past any spaces + comments
        done = False
        while not done and self.pos < len(self.text):
            if (self.text[self.pos].isspace()):
                self.pos += 1
            elif self.pos < len(self.text) - 1 and self.text[self.pos:self.pos + 2] == "//":
                self.pos += 2
                while self.pos < len(self.text) and self.text[self.pos] != "\n":
                    self.pos += 1
                self.pos += 1 #To skip the newline character found
            elif self.pos < len(self.text) - 1 and self.text[self.pos:self.pos + 2] == "/*":
                self.pos + 2
                while self.text[self.pos:self.pos + 2] != "*/":
                    self.pos += 1
                self.pos += 2 #To skip the */
            else:
                done = True

    # Advances to the next token
    # Precondition: Should only be called if has_more_tokens() returns true
    # Sets self.tokentype and self.token
    def advance(self) -> Token:
        if self.text[self.pos].isdigit():
            digits = ""
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                digits += self.text[self.pos]
                self.pos += 1
            token = Token(INT, int(digits))

        elif is_ident_char(self.text[self.pos]):
            token_chars = ""
            while self.pos < len(self.text) and is_ident_char(self.text[self.pos]):
                token_chars += self.text[self.pos]
                self.pos += 1
            if token_chars in self.keywords:
                token_type = KEYWORD
            else:
                token_type = IDENTIFIER
            token = Token(token_type, token_chars)
        elif self.text[self.pos] == '"':
            self.pos += 1
            chars = ""
            while self.text[self.pos] != '"':
                chars += self.text[self.pos]
                self.pos += 1
            self.pos += 1
            token = Token(STR, chars)
        else: #Must be a symbol
            if self.text[self.pos] == "<":
                token = Token(SYMBOL, "&lt;")
            elif self.text[self.pos] == ">":
                token = Token(SYMBOL, "&gt;")
            elif self.text[self.pos] == '"':
                token = Token(SYMBOL, "&quot;")
            elif self.text[self.pos] == "&":
                token = Token(SYMBOL, "&amp;")
            else:
                token = Token(SYMBOL, self.text[self.pos])
            self.pos += 1
        self.eat_whitespace() #Eats up whitespace in preparation for the next token

        return token
    
    def has_more_tokens(self) -> bool:
        return self.cur_token < len(self.tokens)
    
    def next(self) -> Token:
        token = self.tokens[self.cur_token]
        self.cur_token += 1
        return token
    
    def peek(self) -> Token:
        return self.tokens[self.cur_token]
    
    def past(self) -> Token:
        return self.tokens[self.cur_token - 1]
