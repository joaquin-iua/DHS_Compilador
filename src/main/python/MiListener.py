from antlr4 import *
from compiladoresLexer import compiladoresLexer
from compiladoresParser import compiladoresParser
from compiladoresListener import compiladoresListener
from TS import TS

class MiListener(compiladoresListener):
    def __init__(self, output_file):
        super().__init__()
        self.symbol_table = {}
        self.current_context = None
        self.output_file = output_file


    def enterProgram(self, ctx: compiladoresParser.ProgramContext):
        print("Entering program")
        self.symbol_table[self.current_context] = {}

    def exitProgram(self, ctx: compiladoresParser.ProgramContext):
        # self.print_symbol_table()
        print("Exiting program")
        with open(self.output_file, 'w') as file:
            file.write("Tabla de Símbolos:\n")
            for context, symbols in self.symbol_table.items():
                file.write(f"Contexto: {context}\n")
                for variable_name, attributes in symbols.items():
                    file.write(f"  Variable: {variable_name}\n")
                    file.write(f"    Tipo de Dato: {attributes['datatype']}\n")
                    file.write(f"    Inicializada: {attributes['initialized']}\n")
                    file.write(f"    Accedida: {attributes['accessed']}\n")
            print(f"Tabla de Símbolos escrita en {self.output_file}")
            
    def print_symbol_table(self):
        for context, symbols in self.symbol_table.items():
            print(f"Contexto: {context}")
            for symbol_name, symbol_info in symbols.items():
                print(f"[ID: {type(symbol_info)} nombre={symbol_name} tDato={symbol_info['datatype']} inicializado={symbol_info['initialized']} accedido={symbol_info['accessed']}]")

    def enterBlock(self, ctx: compiladoresParser.BlockContext):
        print("Entering block")
        self.current_context = ctx
        self.symbol_table[self.current_context] = {}

    def exitBlock(self, ctx: compiladoresParser.BlockContext):
        if self.current_context in self.symbol_table:
            print("Exiting block")
            del self.symbol_table[self.current_context]
        self.current_context = ctx.parentCtx

    def enterDeclaration(self, ctx: compiladoresParser.DeclarationContext):
        # Verifica si hay un primer hijo en el contexto
        if ctx.getChildCount() >= 2:
            datatype = ctx.getChild(0).getText()
            identifiers = ctx.variable_list().ID()
            for identifier in identifiers:
                identifier_name = identifier.getText()
                symbol = {
                    "datatype": datatype,
                    "initialized": False,
                    "accessed": False,
                    "context": self.current_context
                }
                self.symbol_table[self.current_context][identifier_name] = symbol
                print(f"Declaring {datatype} {identifier_name}")
        else:
            print("Empty declaration")

    def enterAssignment(self, ctx: compiladoresParser.AssignmentContext):
        identifier_name = ctx.ID()
        if identifier_name is not None:
            identifier_name = identifier_name.getText()
            if identifier_name in self.symbol_table[self.current_context]:
                self.symbol_table[self.current_context][identifier_name]["initialized"] = True
                self.symbol_table[self.current_context][identifier_name]["accessed"] = True
                print(f"Assigning value to {identifier_name}")
