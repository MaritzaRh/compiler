from unread_decorator import add_unread
from lexer.Lexer import *


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
        lex = Lexer()
        while True:
            # add decorator to unread a character
            add_unread(fp)
            c = fp.read(1)
            if not c:
                break
            c = c.lower()
            lex.scan(fp, c, tokens, items)
        lex.fill_table("tokens.cvs", tokens, items)
        print("EOF")

Main.main(Main())