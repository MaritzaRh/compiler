import sys
import os
import csv

class Parser():
    def __init__(self):
        input = []
        rule = 0

    def isAMatch(self, headers, input):
        # Look for match between input and headers
        i = 1
        flag = 0
        for header in headers:
            if input == header:
                flag = 1
                break
            i += 1
        i -= 1
        return flag, i

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
            gr = cwd + "\\grammar.txt"
            filegr = open(gr, "r")
        except:
            print("Unexpected error")
            sys.exit()

        headers = []
        grammar = []
        stack = [0]
        data = [row for row in reader]
        #Prepare input
        self.input = items
        self.input.append("$")

        #extract headers from lr table
        for word in filehd:
            word = word.rstrip("\n")
            headers.append(word)
        #extract grammar
        for word in filegr:
            word = word.rstrip("\n")
            grammar.append(word)

        row = -1
        #For each input
        for word in self.input:
            if self.input[0] == "$":
                break
            else:
                #Look for match between input and headers
                flag, i = self.isAMatch(headers, self.input[0])
                #If input and header matched
                if flag:
                    #Take out action> line out from lr table according to input and header: 0-n Ignore 0
                    rule = data[int(stack[-1])][i]
                    #try:
                    if type(rule[0]) != 'int':
                        row = -1
                        lenght = len(rule)
                        aux = []
                        for x in range(1, lenght):
                            aux.append(rule[x])
                        aux = ''.join(map(str, aux))
                        #case shift
                        if rule[0] == 's':
                            stack.append(self.input[0])
                            self.input.remove(self.input[0])
                            stack.append(aux)
                        #case reduce
                        else:
                            print("reduce")
                            production = grammar[int(aux)]
                            production = production.split("->")
                            producer = str(production[0])
                            producer = producer.rstrip(" ")
                            production = production[1]
                            #Case epsilon
                            if production == ' \'\'':
                                stack.append(producer)
                            #Case not epsilon
                            #Case go to
                            flag, i = self.isAMatch(headers, producer)
                            row = int(stack [-2])
                            rule = data[row][i]
                            stack.append(rule)
                    """except:
                        #Empty cell in lr table
                        print("HEREUnexpected token in line ", lines[n])
                        sys.exit()"""
                #Grammar not accepted, header not found
                else:
                    print("Unexpected token in line ", lines[n])
                    sys.exit()
            print(stack)
            print(self.input)
