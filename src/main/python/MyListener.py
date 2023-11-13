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
    currentId = None

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

    #def enterDeclaration(self, ctx: compiladoresParser.DeclarationContext):
        ## guardar currentId a medida que avanza la declaracion para cada variable.
        # print("AL ENTRAR A LA DECLARATION: " + str(ctx.getText()))
        # datatype = str(ctx.getChild(0).getText())
        # name = str(ctx.getChild(0).getText())
        # currentId = Variable(name, datatype)
        # self.symbolsTable.addId(currentId)

    # # cambiarlo a enterDeclaration y no recorrer por examinacion de strings, sino utilizando las habilidades del parser.
    # # guardar los id de la declaracion en la tabla de simbolos con su datatype y name, ademas de una pila que guarde todos los ids de la declaracion.
    # # Luego utilizando la pila y los ids que tiene guardado, habra que asignar los valores que correspondan y esten guardados en la tabla de simbolos.
    # # luego en definition se deben agregar los datos que se les asignen.
    
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
                print(("ID " + id.name + " " + "NOT ADDED: Already exists").center(50, '-'))
            else:
                self.symbolsTable.addId(id)
                print(("ID " + id.name + " " + "ADDED: New identifier").center(50, '-'))
                # currentId = id

    # def exitDefinition(self, ctx: compiladoresParser.DefinitionContext):
    #     # agarrar el currentId, buscarlo en la tabla de simbolos y marcarlo como inicializado.
    #     if(ctx.getText() != ""):
    #         context = self.symbolsTable.findIdGlobal(self.currentId)
    #         if context:
    #             context.symbols[self.currentId.name].setInitialized()
    #         else:
    #             print(self.currentId.name + ": ""Variable is not declared")

    # mejorar para que haga correspondiente a como se generan los arboles y todo.
    def exitAssignment(self, ctx: compiladoresParser.AssignmentContext):
        print("Exiting Assignment".center(80, '*'))
        data = ctx.getText()
        idList = Utils.getIdList(data)

        for nameId in idList:
            Context = self.symbolsTable.findIdGlobal(nameId)
            if Context:
                print("idName: " + nameId + ":" + " IDENTIFIER DECLARED, Assignment done".center(
                    50, '-'))
                print("ANTES DE INICIALIZAR: " + str(Context.symbols[nameId].name))
                Context.symbols[nameId].setInitialized()
                print("DESPUES DE INICIALIZAR: " + str(Context.symbols[nameId].name))
            else:
                print("IDENTIFIER NOT DECLARED, Assignment not done".center(
                    50, '-'))

    def exitFunction_prototype(self, ctx: compiladoresParser.Function_prototypeContext):
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
        context = self.symbolsTable.findIdGlobal(id.name)

        if context:

            if Utils.verifyFunctionPrototype(id):
                print("IMPLEMENTATION MATCHES THE PROTOTYPE".center(50, '-'))
                context.symbols[name].setInitialized()
            else:
                print(
                    "IMPLEMENTATION DOES NOT MATCH THE PROTOTYPE".center(50, '-'))
                
            for id in argsList:
                # PARA LOS PARAMETROS Y ARGUMENTOS DE LAS FUNCIONES, VA EN exitFunction, ->>>>>>>>>>>>>>>>>>>> Verificar
                localContext = self.symbolsTable.findIdLocal(id.name)
                if localContext:
                    print("ENTRE A LOCAL CONTEXT")
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

    # Sobre aca en realidad estan los IDs a verificar si estan accedidos o no.
    def exitFactor(self, ctx: compiladoresParser.FactorContext):
        print("FACTOR: " + str(ctx.getChild(0).getText()))
        idName = ctx.getChild(0).getText()
        context = self.symbolsTable.findIdGlobal(idName)
        # print(str(context))
        if context:
            context.symbols[idName].setAccessed()
    
    # Este es un enfoque no apropiado para verificar accedido, ya que solo devuelve el string de operaciones.
    # def exitArithmetic_logical_op(self, ctx: compiladoresParser.Arithmetic_logical_opContext):
    #     arithmetic_logical_op = ctx.getChild(0)
    #     for child in arithmetic_logical_op.getChildren():
    #         print("QUE HAY EN CHILD: " + child.getText())
    #         if child.getText() == "ID":
    #             variable_name = child.getText()
    #             print("CHILD QUE ES TIPO ID: " + variable_name)
    #             context = self.symbolsTable.findIdGlobal(variable_name)
    #             if context:
    #                 print("IDENTIFIER DECLARED, VARIABLE ACCESSED".center(50, '-'))
    #                 context.symbols[variable_name].setAccessed()
    #                 break
    #             else:
    #                 print("IDENTIFIER NOT DECLARED, VARIABLE NOT ACCESSED".center(50, '-'))


