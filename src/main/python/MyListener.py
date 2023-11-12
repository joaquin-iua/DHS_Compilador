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


class MyListener(compiladoresListener):
    symbolsTable = SymbolsTable()

    # truncate the file
    with FileManager("output/symbolsTable.txt") as STfile:
        STfile.truncate(0)

    def enterProgram(self, ctx: compiladoresParser.ProgramContext):
        print("Entering Program".center(80, "*"))

    def exitProgram(self, ctx: compiladoresParser.ProgramContext):
        print("Exiting Program".center(80, "*"))
        with FileManager("output/symbolsTable.txt") as STfile:
            STfile.write(str(self.symbolsTable.getLastContext()))

    def enterBlock(self, ctx: compiladoresParser.BlockContext):
        print("Entering Block".center(80, "*"))
        self.symbolsTable.addContext()

    def exitBlock(self, ctx: compiladoresParser.BlockContext):
        print("Exiting Block".center(80, "*"))
        with FileManager("output/symbolsTable.txt") as STfile:
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
                id.initialized = True

            if self.symbolsTable.findIdLocal(id.name):
                print('ID NOT ADDED: Already exists'.center(50, '-'))
            else:
                self.symbolsTable.addId(id)
                print('ID ADDED: New identifier'.center(50, '-'))

    def exitAssignment(self, ctx: compiladoresParser.AssignmentContext):
        print("Exiting Assignment".center(80, '*'))
        data = ctx.getText()
        idList = Utils.getIdList(data)

        for nameId in idList:
            Context = self.symbolsTable.findIdGlobal(nameId)
            if Context:
                print("IDENTIFIER DECLARED, Assignment done".center(
                    50, '-'))
                for key in Context.symbols:
                    if key == nameId:
                        Context.symbols[key].initialized = True
                        # Context.symbols[key].accessed = True
            else:
                print("IDENTIFIER NOT DECLARED, Assignment not done".center(
                    50, '-'))

    def exitFunction_Prototype(self, ctx: compiladoresParser.Function_prototypeContext):
        print("Exiting Function Prototype".center(80, '*'))
        datatype = str(ctx.getChild(0).getText())
        data = ctx.getText()[len(datatype):]
        name = Utils.getFunctionName(data)
        argsList = Utils.getFunctionArgs(data)
        id = Function(name, datatype, argsList)

        if self.symbolsTable.findIdLocal(id.name):
            print('ID NOT ADDED: Already exists'.center(50, '-'))
        else:
            self.symbolsTable.addId(id)
            print('ID ADDED: New identifier'.center(50, '-'))

    def exitFunction(self, ctx: compiladoresParser.FunctionContext):
        print("Exiting Function".center(80, '*'))
        datatype = str(ctx.getChild(0).getText())
        data = ctx.getText()[len(datatype):]
        name = Utils.getFunctionName(data)
        argsList = Utils.getFunctionArgs(data)
        id = Function(name, datatype, argsList)

        if self.symbolsTable.findIdGlobal(id.name):

            if Utils.verifyFunctionPrototype(id):
                print("IMPLEMENTATION MATCHES THE PROTOTYPE".center(50, '-'))
            else:
                print(
                    "IMPLEMENTATION DOES NOT MATCH THE PROTOTYPE".center(50, '-'))
        else:
            self.symbolsTable.addId(id)
            print('ID ADDED: New identifier'.center(50, '-'))

    def exitFunctionCall(self, ctx: compiladoresParser.Function_callContext):
        print("Exiting Function Call".center(50, '*'))
        data = ctx.getText()
        nameId = Utils.getFunctionName(data)
        parameters = Utils.getFunctionParameters(data)

        ContextF = self.symbolsTable.findIdGlobal(nameId)

        if ContextF:
            idF = Utils.getId(ContextF, nameId)
            print("Function Prototype found".center(50, '-'))

            if Utils.verifyParameterCount(idF, parameters):
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

    # def exitArithmetic_logical_op(self, ctx: compiladoresParser.Arithmetic_logical_opContext):
    #     arithmetic_logical_op = ctx.getChild(0)
    #     for child in arithmetic_logical_op.getChildren():
    #         if child.getText() == "ID":
    #             variable_name = child.getText()
    #             context = self.symbolsTable.findIdGlobal(variable_name)
    #             if context:
    #                 print("IDENTIFIER DECLARED, VARIABLE ACCESSED".center(50, '-'))
    #                 if variable_name in context.symbols.keys():
    #                     context.symbols[variable_name].accessed = True
    #                     break
    #             else:
    #                 print("IDENTIFIER NOT DECLARED, VARIABLE NOT ACCESSED".center(50, '-'))
