from ID import *
from SymbolsTable import *

class Utils:

    @staticmethod
    def getIdList(data):
        assignment = data.find('=')
        if assignment > 0:
            data = data[:assignment]
        return data.split(',')

    @staticmethod
    def isInitialized(data):
        if data.find('=') > 0:
            if data[data.index('=') + 1:] != '':
                return True
        return False

    @staticmethod
    def getFunctionName(data):
        lpIndex = data.index('(')
        return data[:lpIndex]

    @staticmethod
    def getFunctionArgs(data):
        argsList = []
        lpIndex = data.index('(')
        rpIndex = data.index(')')
        arguments = data[lpIndex + 1:rpIndex].split(',')

        for i in arguments:
            if i[:3] == 'int':
                name = i[3:]
                datatype = 'int'
                argsList.append(Variable(name, datatype, True, True))
            elif i[:6] == 'double':
                name = i[6:]
                datatype = 'double'
                argsList.append(Variable(name, datatype, True, True))
            elif i == '':
                print("FUNCTION ARGUMENT LIST IS EMPTY".center(50, '-'))
        return argsList

    @staticmethod
    def getFunctionParameters(data):
        lpIndex = data.index('(')
        rpIndex = data.index(')')
        return data[lpIndex + 1:rpIndex].split(',')

    @staticmethod
    def verifyFunctionPrototype(id):
        globalContext = SymbolsTable._contextStack[0].symbols
        for i in globalContext:
            if id.name == i:
                id = globalContext[i]
                break
        if id == id:
            return True
        else:
            if id.datatype != id.datatype:
                print("INCORRECT DATA TYPE".center(50, '-'))
                return False
            if id.args != id.args:
                print("INCORRECT ARGUMENT".center(50, '-'))
                return False

    @staticmethod
    def getId(context, parameter) -> ID:
        for key, value in context.symbols.items():
            if key == parameter:
                return value

    @staticmethod
    def verifyParameterQuantity(functionId, parameters) -> True:
        if len(functionId.args) > len(parameters):
            print("NUMBER OF ARGUMENTS DECLARED IN THE PROTOTYPE IS GREATER".center(80, '-'))
            return False
        if len(functionId.args) < len(parameters):
            print("NUMBER OF PARAMETERS IN THE FUNCTION CALL IS GREATER".center(80, '-'))
            return False
        return True
