from antlr4 import *

if "." in __name__:
    from .compiladoresParser import compiladoresParser
else:
    from compiladoresParser import compiladoresParser

from compiladoresListener import compiladoresListener
from SymbolsTable import SymbolsTable
from Context import Context
from ID import *
from Utils import Utils
from FileManager import FileManager
from ErrorsCounter import ErrorsCounter

class MyListener(compiladoresListener):
    symbolsTable = SymbolsTable()
    errorsCounter = ErrorsCounter()

    # truncate the file
    with FileManager("output/symbols_table.txt") as STfile:
        STfile.truncate(0)

    def enterProgram(self, ctx: compiladoresParser.ProgramContext):
        print("Entering Program".center(80, "*"))

    def exitProgram(self, ctx: compiladoresParser.ProgramContext):
        print("Exiting Program".center(80, "*"))
        with FileManager("output/symbols_table.txt") as STfile:
            STfile.write(str(self.symbolsTable.getLastContext()))

    def enterBlock(self, ctx: compiladoresParser.BlockContext):
        print("Entering Block".center(80, "*"))
        self.symbolsTable.addContext()

    def exitBlock(self, ctx: compiladoresParser.BlockContext):
        print("Exiting Block".center(80, "*"))
        with FileManager("output/symbols_table.txt") as STfile:
            STfile.write(str(self.symbolsTable.getLastContext()))
        self.symbolsTable.deleteContext()
    
    def exitDeclaration(self, ctx: compiladoresParser.DeclarationContext):
        print("Exiting Declaration".center(80, "*"))

        datatype = str(ctx.getChild(0).getText())
        data = ctx.getText()[len(datatype):]
        idList = Utils.getIdList(data)

        for i in idList:
            id = Variable(i, datatype)

            if Utils.isInitialized(data):
                 id.setInitialized()

            if self.symbolsTable.findIdLocal(id.name):
                print(("ID " + id.name + " " + "FINDING IF ALREADY DECLARED").center(50, '-'))
                self.errorsCounter.increment()
                
            else:
                self.symbolsTable.addId(id)
                print(("ID " + id.name + " " + "FINDING IF ALREADY DECLARED").center(50, '-'))
                

    def exitAssignment(self, ctx: compiladoresParser.AssignmentContext):
        print("Exiting Assignment".center(80, '*'))
        data = ctx.getText()
        idList = Utils.getIdList(data)

        for nameId in idList:
            Context = self.symbolsTable.findIdGlobal(nameId)
            if Context:
                print("idName: " + nameId + ":" + " FINDING IF ALREADY DECLARED, Assignment type".center(
                    50, '-'))
                print("ANTES DE INICIALIZAR: " + str(Context.symbols[nameId].name))
                Context.symbols[nameId].setInitialized()
                print("DESPUES DE INICIALIZAR: " + str(Context.symbols[nameId].name))
            else:
                print("idName: " + nameId + ":" + " FINDING IF ALREADY DECLARED, Assignment type".center(50, '-'))
                

    def exitFunction_prototype(self, ctx: compiladoresParser.Function_prototypeContext):
        print("Exiting Function Prototype".center(80, '*'))
        datatype = str(ctx.getChild(0).getText())
        data = ctx.getText()[len(datatype):]
        name = Utils.getFunctionName(data)
        argsList = Utils.getFunctionArgs(data)
        
        id = Function(name, datatype, argsList)

        if self.symbolsTable.findIdLocal(id.name):
            print('FINDING IF PARAMETER ALREADY DECLARED'.center(50, '-'))
        else:
            self.symbolsTable.addId(id)
            print('FINDING IF PARAMETER ALREADY DECLARED'.center(50, '-'))

    def exitFunction(self, ctx: compiladoresParser.FunctionContext):
        print("Exiting Function".center(80, '*'))
        datatype = str(ctx.getChild(0).getText())
        data = ctx.getText()[len(datatype):]
        name = Utils.getFunctionName(data)
        argsList = Utils.getFunctionArgs(data)
        id = Function(name, datatype, argsList)
        context = self.symbolsTable.findIdGlobal(id.name)

        if context:

            if Utils.verifyFunctionPrototype(id):
                print("IMPLEMENTATION MATCHES THE PROTOTYPE".center(50, '-'))
                context.symbols[name].setInitialized()
            else:
                print(
                    "IMPLEMENTATION DOES NOT MATCH THE PROTOTYPE".center(50, '-'))
                
                
            for id in argsList:
                localContext = self.symbolsTable.findIdLocal(id.name)
                if localContext:
                    localContext.symbols[id.name].setInitialized()
                    localContext.symbols[id.name].setAccessed()
                else:
                    print("The variable is not defined")
                    


        else:
            self.symbolsTable.addId(id)
            print('ID ADDED: New identifier'.center(50, '-'))

    def exitFunction_call(self, ctx: compiladoresParser.Function_callContext):
        print("Exiting Function Call".center(50, '*'))
        data = ctx.getText()
        nameId = Utils.getFunctionName(data)
        parameters = Utils.getFunctionParameters(data)

        ContextF = self.symbolsTable.findIdGlobal(nameId)

        if ContextF:

            ContextF.symbols[nameId].setAccessed()
            idF = Utils.getId(ContextF, nameId)
            print("Function Prototype found".center(50, '-'))

            if Utils.verifyParameterQuantity(idF, parameters):
                counter = 0
                for id in parameters:
                    ContextP = self.symbolsTable.findIdGlobal(id)
                    if ContextP:
                        print("Parameter ID found".center(50, '-'))
                        idParameter = Utils.getId(ContextP, id)
                        if idParameter.datatype != idF.args[counter].datatype:
                            print("PARAMETER DATA TYPE DOES NOT MATCH THE PROTOTYPE ARGUMENT".center(
                                50, '-'))
                            
                        counter += 1
                    else:
                        print("Parameter ID not found".center(50, '-'))
                        
        else:
            print("Function Prototype not found".center(50, '-'))
            self.errorsCounter.increment()

    def exitFactor(self, ctx: compiladoresParser.FactorContext):
        print("FACTOR: " + str(ctx.getChild(0).getText()))
        idName = ctx.getChild(0).getText()
        context = self.symbolsTable.findIdGlobal(idName)
        # print(str(context))
        if context:
            context.symbols[idName].setAccessed()
    

