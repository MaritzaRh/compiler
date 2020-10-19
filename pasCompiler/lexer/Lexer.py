import csv

class Lexer():
    def __init__(self):
        self.line = 1

    def fill_table(self, file, tokens, items, lines):
        row = 0
        lenght = len(tokens)
        with open(file, 'w', newline='') as f:
            while True:
                writer = csv.writer(f)
                writer.writerow([tokens[row], items[row], lines[row]])
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

    def checkToken(self, fp, c, tokens, items, lines):
        # IS OPERATOR TOKEN
        if c == ';' or c == ',' or c == '.' or c == '{' or c == '}' \
                or c == '(' or c == ')' or c == '[' or c == ']' \
                or c == '+' or c == '*' or c == '-' or c == '/':
            #print("TOKEN - VALUE-> " + c)
            items.append(c)
            tokens.append("TOKEN")
            lines.append(self.line)
        elif c == '=':
            d = fp.read(1)
            if d == '=':
                items.append("EQ")
                tokens.append("TOKEN")
                lines.append(self.line)
                #print("TOKEN - VALUE-> " + c + d)
            else:
                items.append("=")
                tokens.append("TOKEN")
                lines.append(self.line)
                #print("TOKEN - VALUE-> " + c)
        elif c == '<':
            d = fp.read(1)
            if d == '=':
                items.append("LQ")
                tokens.append("TOKEN")
                lines.append(self.line)
                #print("TOKEN - VALUE-> " + c + d)
            elif d == '>':
                items.append("NEQ")
                tokens.append("TOKEN")
                lines.append(self.line)
                #print("TOKEN - VALUE-> " + c + d)
            else:
                items.append(c)
                tokens.append("TOKEN")
                lines.append(self.line)
                #print("TOKEN - VALUE-> " + c)
        elif c == '>':
            d = fp.read(1)
            if d == '=':
                items.append("GE")
                tokens.append("TOKEN")
                lines.append(self.line)
                #print("TOKEN - VALUE-> " + c + d)
            else:
                items.append(c)
                tokens.append("TOKEN")
                lines.append(self.line)
                #print("TOKEN - VALUE-> " + c)
        # IS ASSIGNATION TOKEN
        elif c == ':':
            d = fp.read(1)
            if d == '=':
                items.append(":=")
                tokens.append("TOKEN")
                lines.append(self.line)
                #print("TOKEN - VALUE-> " + c + d)
            else:
                items.append(":")
                tokens.append("TOKEN")
                lines.append(self.line)
                #print("TOKEN - VALUE-> " + c)

    def scan(self, fp, c, tokens, items, lines):
        buffer = []
        if c == '(':
            self.comments(fp, c)
        elif c == '\n':
            self.line += 1
            #if not c:
                #print(self.line)
            #f = fp.tell()
        else:
            self.checkToken(fp, c, tokens, items, lines)

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
                items.append("identifier")
                tokens.append(buffer)
            #print("WORD - LEXEME-> " + buffer.lower())
            lines.append(self.line)
            fp.unread(c)
            if c == '\n':
                self.line += 1
            self.checkToken(fp, c, tokens, items, lines)

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
                lines.append(self.line)
                #print("INTEGER - VALUE-> " + str(integer))
                items.append("identifier")
                tokens.append(c)
                lines.append(self.line)
                #print("WORD - LEXEME-> " + c)
            else:
                buffer = "".join(buffer) + str(integer)
                # append integer and REAL
                if isFloat == 0:
                    items.append(buffer)
                    tokens.append("INTEGER")
                    lines.append(self.line)
                    #print("INTEGER - VALUE-> " + buffer)
                else:
                    items.append(buffer)
                    tokens.append("REAL")
                    lines.append(self.line)
                    #print("REAL - VALUE-> " + buffer)
                #check if the element is token
                self.checkToken(fp, c, tokens, items, lines)
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
            items.append("string")
            tokens.append(buffer)
            lines.append(self.line)
            print("STRING - VALUE-> " + buffer)
