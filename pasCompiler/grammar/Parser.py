import sys
import csv
import os
from unread_decorator import add_unread

class Parser():
    def __init__(self):
        try:
            cwd = os.getcwd()
            cwd = cwd + "\\tokens.cvs"
            fp = open(cwd, "r")
        except:
            print("Unexpected error")
            sys.exit()
