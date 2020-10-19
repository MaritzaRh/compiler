from unread_decorator import add_unread
from lexer.Lexer import *
from grammar.Parser import *

import sys

class Main(Lexer):
    def main(self):
        if len(sys.argv) == 2:
            try:
                fp = open(sys.argv[1], "r")
            except:
                print("Error: incorrect file")
                sys.exit()
        else:
            print("Error: incorrect number of arguments")
            sys.exit()

        items = []
        tokens = []
        lines = []
        lex = Lexer()
        while True:
            # add decorator to unread a character
            add_unread(fp)
            c = fp.read(1)
            if not c:
                break
            c = c.lower()
            lex.scan(fp, c, tokens, items, lines)
        lex.fill_table("tokens.cvs", tokens, items, lines)
        #print("EOF")
        parse = Parser()
        parse.set_lrtable(tokens, items, lines)


Main.main(Main())