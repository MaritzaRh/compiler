import sys
import csv
from unread_decorator import add_unread

class Lexer():
    def __init__(self):
        self.line = 0

    def fill_table(self, file, tokens, items):
        row = 0
        lenght = len(tokens)
        with open(file, 'w', newline='') as f:
            while True:
                writer = csv.writer(f)
                writer.writerow([tokens[row], items[row]])
                row += 1
                if row == lenght:
                    break

    def isReserved(self, buffer):
        flag = False
        keywords = ["program", "constant", "var", "begin", "end", "integer", "real",
                    "boolean", "string", "writeln", "readln", "while", "do", "repeat",
                    "until", "for", "to", "downto", "if", "then", "else",
                    "not", "div", "mod", "and", "or"]
        i = 0
        for word in keywords:
            if keywords[i] == buffer:
                flag = True
                break
            i += 1
        return flag

    def comments(self, fp, c):
        # COMMENTS
        current = fp.read(1)
        if current == '*':
            current = fp.read(1)
            next = fp.read(1)
            while current != '*' and next != ')':
                current = next
                next = fp.read(1)
        else:
            fp.unread(current)

    def checkToken(self, fp, c, tokens, items):
        # IS OPERATOR TOKEN
        if c == ';' or c == ',' or c == '.' or c == '{' or c == '}' \
                or c == '(' or c == ')' or c == '[' or c == ']' \
                or c == '+' or c == '*' or c == '-' or c == '/':
            print("TOKEN - VALUE-> " + c)
            items.append(c)
            tokens.append("TOKEN")
        elif c == '=':
            d = fp.read(1)
            if d == '=':
                items.append("EQ")
                tokens.append("TOKEN")
                print("TOKEN - VALUE-> " + c + d)
            else:
                items.append("=")
                tokens.append("TOKEN")
                print("TOKEN - VALUE-> " + c)
        elif c == '<':
            d = fp.read(1)
            if d == '=':
                items.append("LQ")
                tokens.append("TOKEN")
                print("TOKEN - VALUE-> " + c + d)
            elif d == '>':
                items.append("NEQ")
                tokens.append("TOKEN")
                print("TOKEN - VALUE-> " + c + d)
            else:
                items.append(c)
                tokens.append("TOKEN")
                print("TOKEN - VALUE-> " + c)
        elif c == '>':
            d = fp.read(1)
            if d == '=':
                items.append("GE")
                tokens.append("TOKEN")
                print("TOKEN - VALUE-> " + c + d)
            else:
                items.append(c)
                tokens.append("TOKEN")
                print("TOKEN - VALUE-> " + c)
        # IS ASSIGNATION TOKEN
        elif c == ':':
            d = fp.read(1)
            if d == '=':
                items.append(":=")
                tokens.append("TOKEN")
                print("TOKEN - VALUE-> " + c + d)
            else:
                items.append(":")
                tokens.append("TOKEN")
                print("TOKEN - VALUE-> " + c)

    def scan(self, fp, c, tokens, items):
        if c == '(':
            self.comments(fp, c)
        elif c == '\n':
            self.line += 1
            c = fp.read(1)
            #if not c:
                #print(self.line)
            #f = fp.tell()
        else:
            self.checkToken(fp, c, tokens, items)
        buffer = []
        # IS ID
        if c.isalpha():
            while c.isdigit() or c.isalpha():
                buffer.append(c)
                c = fp.read(1)
            buffer = "".join(buffer)
            if self.isReserved(buffer):
                items.append(buffer)
                tokens.append("RESERVED")
            else:
                items.append(buffer)
                tokens.append("ID")
            print("WORD - LEXEME-> " + buffer.lower())
            fp.unread(c)
            self.checkToken(fp, c, tokens, items)
        # IS NUMBER
        elif c.isdigit():
            integer = 0
            isFloat = 0
            while c.isdigit():
                integer *= 10
                integer += int(c)
                c = fp.read(1)
            if c == '.':
                buffer.append(str(integer))
                buffer.append(c)
                integer = 0
                c = fp.read(1)
                isFloat = 1
                while c.isdigit():
                    integer *= 10
                    integer += int(c)
                    c = fp.read(1)
            if c.isalpha():
                #case number is 1e
                items.append(str(integer))
                tokens.append("INTEGER")
                print("INTEGER - VALUE-> " + str(integer))
                items.append(c)
                tokens.append("ID")
                print("WORD - LEXEME-> " + c)
            else:
                buffer = "".join(buffer) + str(integer)
                # append integer and REAL
                if isFloat == 0:
                    items.append(buffer)
                    tokens.append("INTEGER")
                    print("INTEGER - VALUE-> " + buffer)
                else:
                    items.append(buffer)
                    tokens.append("REAL")
                    print("REAL - VALUE-> " + buffer)
                #check if the element is token
                self.checkToken(fp, c, tokens, items)
        # IS STRING
        elif c == '\'' or c == '\"':
            buffer.append(c)
            c = fp.read(1)
            while True:
                buffer.append(c)
                c = fp.read(1)
                if c == '\'' or c == '\"':
                    break
            buffer.append(c)
            buffer = "".join(buffer)
            items.append(buffer)
            tokens.append("CHARACTERSTRING")
            print("STRING - VALUE-> " + buffer)
