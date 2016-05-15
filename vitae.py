import re
import sys
import os
import time
class vitMath(object):
    def __init__(self):
        main = Vitae()

    def inc(self,line,vars1,vars2):
        """
        inc() - accepts the line and variable name and value to increment
        """
        everything = []
        vars1 = dict(vars1)
        vars2 = dict(vars2)
        if re.match(main.Vkb['incVar'],line):
            for k in vars2.keys():
                if main.findWholeWord(k)(line):
                        increasedValue = int(vars2[k]) + 1
                        variableName = k
                        everything.append(variableName)
                        everything.append(str(increasedValue))
            for k in vars1.keys():
                if main.findWholeWord(k)(line):
                        increasedValue = int(vars1[k]) + 1
                        variableName = k
                        everything.append(variableName)
                        everything.append(str(increasedValue))

        return tuple(everything)

    def dec(self,line,vars1,vars2):
        everything = []
        vars1 = dict(vars1)
        vars2 = dict(vars2)
        if re.match(main.Vkb['decVar'],line):
            for k in vars2.keys():
                if main.findWholeWord(k)(line):
                        decreasedValue = int(vars2[k]) - 1
                        variableName = k
                        everything.append(variableName)
                        everything.append(str(decreasedValue))
            for k in vars1.keys():
                if main.findWholeWord(k)(line):
                        decreasedValue = int(vars1[k]) - 1
                        variableName = k
                        everything.append(variableName)
                        everything.append(str(decreasedValue))
        return tuple(everything)


class Vitae():
    def __init__(self):
        self.Scopes = {
            'born':'die',
            'times':'done'
            }
        self.types = {
            'int':  lambda x: int(x),
            'str':  lambda x: str(x),
            'list': lambda x: list(x),
            'tuple':    lambda x: tuple(x),
            'ord':  lambda x: ord(x)
            }
        self.Vkb = {
            'keywords':{
                'born',
                'die',
                'thing',
                'say',
                'is',
                'done',
                'times',
                'listen',
                'into',
                'int',
                'str',
                'tuple',
                'list',
                'ord'
                },
            'spaceTab':r'[\t ]*?$',
            'start':r'^[\t ]*?born[\t ]*?$',
            'end':r'^[\t ]*?die[\t ]*?$',
            'print':r'^[\t ]*?say[\t ]*?.*?$',
            'listen':r'^[\t ]*?listen([(][\t ]*?["]([\t\n \x20-\x7F]*?)["][\t ]*?[)])?[\t ]+.*?$',
            'things':r'^[\t ]*?thing[\t ]*?.*?$',
            'done':r'^[\t ]*?done[\t ]*?$',
            'times':r'^.*?times[\t ]*?$',
            'listenInput':r'^[\t ]*?listen[\t ]+?into[\t ]+?([A-z_]+[0-9]*[A-z_]*?)+?[\t ]*?$',
            'listenMsg':r'^[\t ]*?listen[\t ]*?[\(][\t ]*?["]([\t\n \x20-\x7F]*?)["][\t ]*?[\)]?[\t ]+?into[\t ]+?([A-z_]+[0-9]*[A-z_]*?)+?[\t ]*?$',
            'thingsInt':r'^[\t ]*?thing[\t ]+([A-z_]+[0-9]*[A-z_]*?)+?[\t ]+?is[\t ]+?([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)[\t ]*?$',
            'thingsStr':r'^[\t ]*?thing[\t ]+([A-z_]+[0-9]*[A-z_]*?)+?[\t ]+is[\t ]+["]([\t\n \x20-\x7F]*?)["][\t ]*?$',
            'thingsThings':r'^[\t ]*?thing[\t ]+?([A-z_]+[0-9]*[A-z_]*?)+?[\t ]+?is[\t ]+?(([A-z_]+[0-9]*[A-z_]*?)+?)[\t ]*?$',
            'timesVar':r'^[\t ]*?([A-z_]+[0-9]*[A-z_]*?)+?[\t ]+?times[\t ]*?$',
            'timesInt':r'^[\t ]*?([0-9]+)+?[\t ]+?times[\t ]*?$',
            'strings':r'^.*["]([\t\n \x20-\x7F]*?)["].*$',
            'inc': r'^[\t ]*?inc\(.*\)[\t ]*?$',
            'dec': r'^[\t ]*?dec\(.*\)[\t ]*?$',
            'incInt':r'^[\t ]*?inc\([0-9]*\)[\t ]*?$',
            'incVar':r'^[\t ]*?inc\([\t ]*?([A-z_]+[0-9]*?[A-z_]*?)+?\)[\t ]*?$',
            'decVar':r'^[\t ]*?dec\([\t ]*?([A-z_]+[0-9]*?[A-z_]*?)+?\)[\t ]*?$'
            }
        self.FuncVkb = {
            'printStr':r'^[\t ]*?say[\t ]+?["]([\t\n \x20-\x7F]*)["][\t ]*?$',
            'printVar':r'^[\t ]*?say[\t ]+?([A-z_]+[0-9]*[A-z_]*?)+[\t ]*?$',
            'printExc':r'^[\t ]*?say[\t ]+?([\t\n \x20-\x7F]*?)[\t ]*?$',
            'printComboStr':r'^[\t ]*?say[\t ]+?["]([\t\n \x20-\x7F]*)["]+([\t ]*?[,] [\t ]*?["]([\t\n \x20-\x7F]*)["]+)+[\t ]*?$',
            'printComboVar':r'^[\t ]*?say[\t ]+?([A-z_]+[0-9]*[A-z_]*?)+([\t ]*?[,] [\t ]*?([A-z_]+[0-9]*[A-z_]*?)+)+[\t ]*?$'
            }

        self.ErrorCodes = {
            'Life':{
                'CriticalError':"Error:\nThe problem seems to persist in the Life of the program! Please check the structure of the Life! (.i.e. born and die statements etc.)",
                'Born':"Error:\nThe born statement was not found!",
                'Die':"Error:\nThe die statement was not found!",
                'Times':{
                    'PairError':"Error:\nThe times and done statements should always occur in pairs!",
                    'ZeroTimes':"Error:\nThere can't be a 0 times loop, Sorry.",
                    'TypeError':"Error:\nThe syntax in the times command is wrong"
                    },

                },
            'Listen':{
                'Error':'Error:\nThe syntax of the listen statement is wrong.'
                },
            'Thing':{
                'Warning':{
                    'Unused':"Warning:\nThe thing wasn't even used in the Life! c'mon man!"
                    },
                'Error':{
                    'Assignment':"Error:\nThe thing is not properly assigned in the structure of the Life!",
                    'Keyword':"Error:\nThing cannot be assigned to the name of a keyword"
                    }
                },
            'Say':{
                ''
                },
            'Math':{
            'inc':'increment value can only be an integer'
            }

            }
        self.counter = 0
        self.sf = 0
        self.ef = 0
        self.varStr = []
        self.varInt = []
        self.DictVarStr = {}
        self.DictVarInt = {}
        self.text = []
        self.input = ""
        self.varsUpdate()

    """
    HELPER FUNCTIONS STARTS ---------------
    """
    def bug(self,msg):
        if 'Warning' in msg:
            print(msg)
        else:
            sys.exit(msg)

    def debug(self):
        print "\n######################## DEBUG ########################\n"
        print "\nvarsStr:\n"
        for i in self.DictVarStr.keys(),self.DictVarStr.values():
            print i
        print "\nvarsInt:\n"
        for i in self.DictVarInt.keys(),self.DictVarInt.values():
            print i
        print "\nScopes:\n"
        for i in self.Scopes.keys():
                print self.getScope(i,self.Scopes[i])

    def escapeSeq(self,string):
        try:
            return string.replace('\\n','\n').replace('\\t','\t').replace('\\f','\f').replace('\\b','\b').replace('\\a','\a')
        except:
            return string

    def findWholeWord(self,word):
        try:
            return re.compile(r'\b({0})\b'.format(word)).search
        except:
            return w

    def listToDict(self,this):
        keys = []
        values = []
        for i in range(0,len(list(this))):
            keys.append(this[i][0])
            values.append(this[i][1])
        return dict(zip(keys,values))

    def varsUpdate(self):
        self.DictVarStr = self.listToDict(self.varStr)
        self.DictVarInt = self.listToDict(self.varInt)

    """
    HELPER FUNCTIONS ENDS ---------------
    """

    def listen(self, line):
        if re.match(self.Vkb['listenMsg'],line):
            inputVar2 =  re.findall(self.Vkb['listenMsg'],line)
            inputList = []
            message = inputVar2[0][0]
            variable = inputVar2[0][1]
            if message:
                message = self.escapeSeq(message)
                value = self.getInput(message)
                inputList.append(variable)
                inputList.append(value)
                self.varStr.append(tuple(inputList))
                self.varsUpdate()
            else:
                value = self.getInput()
                inputList.append(variable)
                inputList.append(value)
                self.varStr.append(tuple(inputList))
                self.varsUpdate()
        else:
            self.bug(self.ErrorCodes['Listen']['Error'])

    def execute(self,func,line):
        """
        execute() - Executes different functions of Vitae
        Params - two parameters 'func,lineOfText'
        Returns - the executed part
        """
        if re.match(self.FuncVkb[func],line):
            string = re.findall(self.FuncVkb[func],line)
            return string
        elif not re.match(self.FuncVkb[func],line):
            return None

    def times(self):
        """
        TODO - REFACTOR THE METHOD
        """
        howManyTimes = 0
        timesConst,timesScopes = self.getScope('times','done')
        for scope in timesScopes:
            if(re.findall(self.Vkb['timesInt'],self.text[scope[0]-1])):
                howManyTimes = re.findall(self.Vkb['timesInt'],self.text[scope[0]-1])
                howManyTimes = int(howManyTimes[0])

            if(re.findall(self.Vkb['timesVar'],self.text[scope[0]-1])):
                for k in self.DictVarStr.keys():
                    if self.findWholeWord(k)(self.text[scope[0]-1]):
                        howManyTimes = re.sub(r'\b({0})\b'.format(k),self.DictVarStr[k] , self.text[scope[0]-1]).split(" ")
                howManyTimes = int(howManyTimes[0])

            for repeat in range(0,howManyTimes-1):
                self.read(scope[0],scope[1])

    def printing(self,i):
        """
        printing() - Decides the various functions to be used in the life
        Params - lineOfText
        Returns - None
        """
        if self.execute('printStr', i):
            string = self.execute('printStr',i)
            for char in string:
                print self.escapeSeq(char)
        elif self.execute('printVar', i):
            self.printSwapVar(i,False)
        elif self.execute('printComboVar', i):
            self.printSwapVar(i,True)

    def printSwapVar(self,i,comboBol = False):
        """
        printSwaVar()- Swaps the variables in the say func and prints the values
        Params - the line on which the say func occurs
        Returns - prints out the value
        """
        printingCombo = ""
        if comboBol == False:
            if self.DictVarStr.keys():
                for k in self.DictVarStr.keys():
                    if self.findWholeWord(k)(i):
                        i = re.sub(r'\b({0})\b'.format(k),self.DictVarStr[k] , i)
                        r = self.execute('printExc',i)
                        if r != None:
                            for j in r:
                                print j
                if self.DictVarInt.keys():
                    for k in self.DictVarInt.keys():
                        if self.findWholeWord(k)(i):
                            i = re.sub(r'\b({0})\b'.format(k),self.DictVarInt[k] , i)
                            r = self.execute('printExc',i)
                            for j in r:
                                print j
            else:
                if self.DictVarInt.keys():
                    for k in self.DictVarInt.keys():
                                if self.findWholeWord(k)(i):
                                    i = re.sub(r'\b({0})\b'.format(k),self.DictVarInt[k] , i)
                                    r = self.execute('printExc',i)
                                    for j in r:
                                        print j
                else:
                    for k in self.DictVarStr.keys():
                        if self.findWholeWord(k)(i):
                            i = re.sub(r'\b({0})\b'.format(k),self.DictVarStr[k] , i)
                            r = self.execute('printExc',i)
                            for j in r:
                                print j
        else:
            if comboBol == True:
                i = i.replace(',','')   #   replaces the commas between variables in say statement (useful for swapping values)
                if self.DictVarStr.keys():
                    for k in self.DictVarStr.keys():
                        if self.findWholeWord(k)(i):
                            i = re.sub(r'\b({0})\b'.format(k),self.DictVarStr[k] , i)
                            r = self.execute('printExc',i)
                            if r != None:
                                for j in r:
                                    printingCombo = j
                    if self.DictVarInt.keys():
                        for k in self.DictVarInt.keys():
                            if self.findWholeWord(k)(i):
                                i = re.sub(r'\b({0})\b'.format(k),self.DictVarInt[k] , i)
                                r = self.execute('printExc',i)
                                for j in r:
                                    printingCombo = j
                else:
                    if self.DictVarInt.keys():
                        for k in self.DictVarInt.keys():
                                    if self.findWholeWord(k)(i):
                                        i = re.sub(r'\b({0})\b'.format(k),self.DictVarInt[k] , i)
                                        r = self.execute('printExc',i)
                                        for j in r:
                                            printingCombo = j
                    else:
                        for k in self.DictVarStr.keys():
                            if self.findWholeWord(k)(i):
                                i = re.sub(r'\b({0})\b'.format(k),self.DictVarStr[k] , i)
                                r = self.execute('printExc',i)
                                for j in r:
                                    printingCombo = j
            print printingCombo

    def getInput(self,message=""):
        """
        getInput() - Takes the input in with the help of the input command and performs various input operations
        Params - Takes a message
        Returns - returns the outputStream
        TODO - (OPTIONAL) implicitly type-cast the inputStream to a standard
        """
        return raw_input(self.escapeSeq(message))


    def typeOf(self,inputStream):
        """
        TODO - IMPLEMENT IT !
        """
        return type(inputStream)


    def encryptStr(self):
        """
        encryptStr() - encrypts the string values used in the program to a standard so as to avoid interpreter confusion and enabling security
        """
        listOfStrings = []
        for i in self.text:
            if(re.match(self.Vkb['strings'],i)):
                listOfStrings.append(re.findall(self.Vkb['strings'],i))
        return listOfStrings


    def getScope(self, start, end):
        """
        getScope() - This returns the scope b/w the starting and the end param of the text
        Params - start, end -> pairs of starting and ending scope characters
        Returns - returns the text b/w the "start, end" along with the their line numbers
        """
        c = 1
        sc = []
        scopeNos = []
        sf = 0
        scope = []
        for i in self.text:
            if self.findWholeWord(start)(i):
                sc.append(c)
                sf = 1
            if self.findWholeWord(end)(i) and sf == 1:
                    scope.append(self.text[(sc[-1]-1):self.text.index(i)+1])
                    scopeNos.append([(sc[-1]),(self.text.index(i)+1)])
                    sc.pop()
            c = c + 1
        scopeNos = scopeNos[::-1]
        return scope,scopeNos


    def varCheck(self):
        """
        TODO - REFACTOR METHOD
        """
        """
        varCheck() - checks the variables used in the program to see the following-
                        1. whether they are initialized or not
                        2. whether they are the keywords or not
                        3. whether they are used or not
        Returns - None
        """
        varUsed = []
        for variables in self.DictVarInt.keys(),self.DictVarStr.keys():            # Checking for keywords used as variable names
            for variable in variables:
                for keywords in self.Vkb['keywords']:
                    if variable == keywords:
                        sys.exit(self.ErrorCodes['Thing']['Error']['Keyword'])
                for lines in self.text:                                                 # Checking if the variable was used ever after initialization
                    if not re.match(self.Vkb['thingsStr'],lines):
                        if not re.match(self.Vkb['thingsInt'],lines):
                            if self.findWholeWord(variable)(lines):
                                varUsed.append(variable)
        variable= list(self.DictVarInt.keys()+self.DictVarStr.keys())
        usage = [item for item in variable if item not in varUsed]

        if not len(usage) == 0:
            self.bug(self.ErrorCodes['Thing']['Warning']['Unused'])


    def checkInLife(self,checkWhat):
            """
            checkInLife() - checks the program (life) is in correct form
            Params - checks a language construct
            Returns - no of constructs present in the program
            """
            noOf = []
            for i in self.text:
                try:
                    noOf.append(re.match(self.Vkb[checkWhat],i).group())
                except:
                    pass
            return len(noOf)


    def preProcess(self):
        """
        preProcess() - Performs the preprocessing of the program file to check for mandatory constructs of Vitae
        Params - content of a file
        Returns - None, (sets the various flag for others modules)
        """
        if self.checkInLife('start') != 1 or self.checkInLife('end') != 1:
            self.bug(self.ErrorCodes['Life']['CriticalError'])

        if self.checkInLife('times') != self.checkInLife('done'):
            self.bug(self.ErrorCodes['Life']['Times']['PairError'])
            
        for i in self.text:
            if not re.match(self.Vkb['spaceTab'],i):            #indicates a written language construct is present

                if re.match(self.Vkb['start'],i) and self.sf == 0:    #checks for the starting of the program
                    self.sf = 1                                 # indicates the start of the program, should cache this line.
                
                if self.sf == 0:
                    self.bug(self.ErrorCodes['Life']['Born'])

                if re.match(self.Vkb['things'],i) and self.sf == 1:
                    if re.match(self.Vkb['thingsInt'],i):
                        self.varInt.append(re.findall(self.Vkb['thingsInt'],i)[0])
                    else:
                        if re.match(self.Vkb['thingsStr'],i):
                            self.varStr.append(re.findall(self.Vkb['thingsStr'],i)[0])
                        elif not re.match(self.Vkb['thingsStr'],i):
                            self.bug(self.ErrorCodes['Thing']['Error']['Assignment'])
                
                if re.match(self.Vkb['end'],i) and self.sf == 1:
                    self.ef = 1
        
                if i == self.text[-1]:
                    if re.match(self.Vkb['end'],i) and self.sf == 1:
                        self.ef = 1

                    if self.ef == 0:
                        self.bug(self.ErrorCodes['Life']['Die'])

                    if not re.match(self.Vkb['end'],i):
                        self.bug(self.ErrorCodes['Life']['CriticalError'])                        
                    
        self.varsUpdate() 
        self.varCheck()


    def read(self,startpos,endpos):
        """
        read(startpos, endpos) - reads the input file text between a start position to end postion
        Params - start position, end position
        Returns - None 
        """
        self.preProcess()

        for i in self.text[startpos:endpos]:
            if not re.match(self.Vkb['spaceTab'],i):            #indicates a written language construct is present
                if re.match(self.Vkb['listen'],i):
                    self.listen(i)

                elif re.match(self.Vkb['times'],i):
                    self.times()

                elif re.match(self.Vkb['inc'], i):
                    self.varStr.append(
                        vitMath().inc(i,self.DictVarInt,self.DictVarStr)
                        )
                    self.varsUpdate()

                elif re.match(self.Vkb['dec'], i):
                    self.varStr.append(
                        vitMath().dec(i,self.DictVarInt,self.DictVarStr)
                        )
                    self.varsUpdate()

                elif re.match(self.Vkb['print'],i):
                    self.printing(i)
            self.counter = self.counter + 1


    def reader(self,fileName):
        """
        reader() - reads the entire structure of the program and performs the interpretation.
        Params - File Name of the program
        Returns - None
        """
        file = open(fileName,'r')
        self.text = file.readlines()
        file.close()

        print "-> Program started:",fileName,'\n\n'
        startTime = time.time()

        self.read(0,len(self.text))
        endTime = time.time()
        print "\n\n-> Program Completed in: ",(endTime-startTime),"s"


    def init(self):
        """
        init() - initiates the command-line reading and the interpreter
        Params - None
        Returns  - None
        """
        if (len(sys.argv)>3 or len(sys.argv)<3):
            print("USAGE: vitae.py -c (filename)")
        elif(len(sys.argv)==3):
            filePath = os.path.abspath(sys.argv[2])
            self.reader(filePath)
            # self.debug()
v = Vitae()
v.init()

