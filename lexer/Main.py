import sys
import csv
import tokenize
from unread_decorator import add_unread


def fill_table(file, tokens, items):
    row = 0
    lenght = len(tokens)
    with open(file, 'w', newline='') as f:
        while True:
            writer = csv.writer(f)
            writer.writerow([tokens[row], items[row]])
            row += 1
            if row == lenght:
                break

def isReserved(buffer):
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


def spaces(fp, c):
    # SPACES
    while c == ' ' or c == ',':
        c = fp.read(1)
    return c


def comments(fp, c):
    # COMMENTS
    if c == '(':
        current = fp.read(1)
        if current == '*':
            current = fp.read(1)
            next = fp.read(1)
            while current != '*' and next != ')':
                current = next
                next = fp.read(1)
            c = fp.read(1)
            return 1
        else:
            fp.unread(c)
            return 0


def newLine(fp, c, line):
    # NEW LINE
    if c == '\n':
        line += 1
    fp.unread(c)


def checkToken(fp, c, tokens, items):
    # IS OPERATOR TOKEN
    c = fp.read(1)
    if c == ';' or c == ',' or c == '.' or c == '{' or c == '}' \
            or c == '(' or c == ')' or c == '[' or c == ']' \
            or c == '+' or c == '*' or c == '-' or c == '/':
        print("TOKEN - VALUE-> " + c)
        items.append(c)
        tokens.append("TOKEN")
        fp.unread(c)
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
        fp.unread(d)
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
        fp.unread(d)
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
        fp.unread(d)
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
        fp.unread(d)
    fp.unread(c)


def scan(fp, c, line, tokens, items):
    comments(fp, c)
    c = spaces(fp, c)
    newLine(fp, c, line)
    checkToken(fp, c, tokens, items)

    c = fp.read(1)
    buffer = []

    # IS ID
    if c.isalpha():
        while c.isdigit() or c.isalpha():
            buffer.append(c)
            c = fp.read(1)
        buffer = "".join(buffer)
        if isReserved(buffer):
            items.append(buffer)
            tokens.append("RESERVED")
        else:
            items.append(buffer)
            tokens.append("ID")
        print("WORD - LEXEME-> " + buffer)
        fp.unread(c)
        checkToken(fp, c, tokens, items)
        newLine(fp, c, line)

    # IS NUMBER
    elif c.isdigit():
        integer = 0
        buffer = []
        flag = 0
        while c.isdigit():
            integer *= 10
            integer += int(c)
            c = fp.read(1)
        if c == '.':
            buffer.append(str(integer))
            buffer.append(c)
            integer = 0
            c = fp.read(1)
            flag = 1
            while c.isdigit():
                integer *= 10
                integer += int(c)
                c = fp.read(1)
        if c.isalpha():
            items.append(str(integer))
            tokens.append("INTEGER")
            print("INTEGER - VALUE-> " + str(integer))
            items.append(c)
            tokens.append("ID")
            print("WORD - LEXEME-> " + c)
        else:
            buffer = "".join(buffer) + str(integer)
            # REAL
            if flag == 0:
                items.append(buffer)
                tokens.append("INTEGER")
                print("INTEGER - VALUE-> " + buffer)
            else:
                items.append(buffer)
                tokens.append("REAL")
                print("REAL - VALUE-> " + buffer)
        newLine(fp, c, line)

    # IS STRING
    elif c == '\'' or c == '\"':
        buffer = []
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
        newLine(fp, c, line)


def main():
    if sys.argv[1]:
        try:
            fp = open(sys.argv[1], "r")
        except:
            print("error: not a valid file")
            exit()
    else:
        print("error: invalid number of arguments")
        exit()

    line = 0
    items = []
    tokens = []
    while True:
        # add decorator to unread a character
        add_unread(fp)
        c = fp.read(1)
        if not c:
            break
        c = c.lower()
        scan(fp, c, line, tokens, items)
    fill_table("tokens.cvs", tokens, items)
    print("EOF")

    """pieces = []
    with tokenize.open(sys.argv[1]) as file:
        tokens = tokenize.generate_tokens(file.readline)
        for token in tokens:
            pieces.append(token.line)
    print(pieces)"""


main()
