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
            #print(i,header,input)
            if input == header:
                flag = 1
                break
            i += 1
        i -= 1
        return flag, i

    def printError(self, acc, originalInputLen, tokens, stack, lines):
        inputLen = len(self.input)
        #all input read
        if not acc:
            error = originalInputLen - inputLen
            lineError = str(lines[error])
            tkerror = self.input[0]
        else:
            error = originalInputLen - inputLen - 2
            lineError = str(lines[error+1])
            tkerror = stack[-2]
        if tkerror == 'identifier' or tkerror == 'integer' or tkerror == 'real':
            tkerror = str(tokens[error])
            print("id, int or real")
            if tkerror == 'RESERVED':
                tkerror = str(tokens[error + 2])
        print("main.pas(" + lineError + ") Fatal: Syntax error, unexpected token \"" + tkerror + "\"" + "\nFatal: Compilation aborted" + "\nError: /usr/bin/ppcx64 returned an error exitcode (normal if you did not specify a source file to be compiled)")
        sys.exit()

    def analyzeGrammar(self, tokens, items, lines):
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
        #self.input.append(".")
        self.input.append("$")

        #extract headers from lr table
        for word in filehd:
            word = word.rstrip("\n")
            headers.append(word)
        #extract grammar
        for word in filegr:
            word = word.rstrip("\n")
            grammar.append(word)

        originalInputLen = len(self.input)

        acc = True

        row = -1
        #For each input
        while True:
            if not self.input[0] or stack[0] == 'programa':
                break
            else:
                #Look for match between input and headers
                flag, i = self.isAMatch(headers, self.input[0])
                #If input and header matched
                if flag:
                    #Take out action> line out from lr table according to input and header: 0-n Ignore 0
                    rule = data[int(stack[-1])][i]
                    #empty cell
                    if not rule:
                        acc = False
                        self.printError(acc, originalInputLen, tokens, stack, lines)
                    elif rule == 'acc':
                        break
                    try:
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
                                production = grammar[int(aux)]
                                production = production.split("->")
                                producer = str(production[0])
                                producer = producer.rstrip(" ")
                                production = production[1]
                                #Case epsilon
                                if production == ' \'\'':
                                    stack.append(producer)
                                #Case not epsilon
                                else:
                                    production = production.split(' ')
                                    production.remove(production[0])
                                    for element in production:
                                        stack.pop()
                                        if not stack:
                                            break
                                        stack.pop()
                                    stack.append(producer)
                                #Case go to
                                flag, i = self.isAMatch(headers, producer)
                                try:
                                    row = int(stack[-2])
                                except:
                                    pass
                                rule = data[row][i]
                                stack.append(rule)
                    except:
                        #Empty cell in lr table
                        acc = False
                        self.printError(acc, originalInputLen, tokens, stack, lines)
                #Grammar not accepted, header not found
                else:
                    acc = False
                    self.printError(acc, originalInputLen, tokens, stack, lines)
        print("Program finished with exit code 0")
