from antlr4 import *
from compiladoresListener import compiladoresListener
from compiladoresParser   import compiladoresParser
from Clases import TS, Contexto, ID, Funcion, Variable

class miListener(compiladoresListener) :

    # Enter a parse tree produced by compiladoresParser#programa.
    def enterProgram(self, ctx:compiladoresParser.ProgramContext):
        print("Comenzando la compilacion")
        print("\t" + ctx.getText())

    # Exit a parse tree produced by compiladoresParser#programa.
    def exitProgram(self, ctx:compiladoresParser.ProgramContext):
        print("FIN de la compilacion")
        print("\t" + ctx.getText())
 
     # Enter a parse tree produced by compiladoresParser#bloque.
    def enterBlock(self, ctx:compiladoresParser.BlockContext):
        print("Inicio bloque")

    # Exit a parse tree produced by compiladoresParser#bloque.
    def exitBlock(self, ctx:compiladoresParser.BlockContext):
        # print("\tBloque con " + str(ctx.getChildCount()) + " hijos" )
        # print("\t --> " + ctx.getText())
        print("FIN bloque")

    def exitDeclaration(self, ctx:compiladoresParser.DeclarationContext):
        print("\tTipo dato : " + str(ctx.getChild(0)))
        print("\tnombre var: " + str(ctx.getChild(1)))

    # def enterEveryRule(self, ctx: ParserRuleContext):
    #     return super().enterEveryRule(ctx)
    
    # def visitTerminal(self, node: TerminalNode):
    #     print(" ---> Hoja --> " + str(node))