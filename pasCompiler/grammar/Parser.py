import sys
import os
import csv
from itertools import islice

class Parser():
    def __init__(self):
        input = []
        rule = 0

    def set_lrtable(self, tokens, items, lines):
        try:
            #Open LR table
            cwd = os.getcwd()
            lr = cwd + "\\lrtable.csv"
            lrtable = open(lr, "r")
            reader = csv.reader(lrtable)
            #Open headers of LR table
            hd = cwd + "\\headers.txt"
            filehd = open(hd, "r")
        except:
            print("Unexpected error")
            sys.exit()

        headers = []
        stack = [0]
        data = [row for row in reader]
        #Prepare input
        self.input = items
        self.input.append("$")

        #extract headers from lr table
        for word in filehd:
            word = word.rstrip("\n")
            headers.append(word)

        n = 0
        #For each input
        for word in self.input:
            if self.input[n] == "$":
                break
            else:
                #Look for match between input and headers
                i = 1
                flag = 0
                for header in headers:
                    if self.input[n] == header:
                        flag = 1
                        break
                    i += 1
                i -= 1
                #If input and header matched
                if flag:
                    #Take out action> line out from lr table according to input and header: 0-n Ignore 0
                    print(stack[-1])
                    print(i)
                    rule = data[int(stack[-1])][i]
                    print(rule)
                    #try:
                    if type(rule[0]) == 'int':
                        print("goto")
                    else:
                        lenght = len(rule)
                        aux = []
                        #case shift
                        if rule[0] == 's':
                            stack.append(self.input[0])
                            self.input.remove(self.input[0])
                            for x in range(1, lenght):
                                aux.append(rule[x])
                            aux = ''.join(map(str, aux))
                            stack.append(aux)
                        #case reduce
                        else:
                            print("reduce")
                    """except:
                        #Empty cell in lr table
                        print("HEREUnexpected token in line ", lines[n])
                        sys.exit()"""
                #Grammar not accepted, header not found
                else:
                    print("Unexpected token in line ", lines[n])
                    sys.exit()
            print(stack)

