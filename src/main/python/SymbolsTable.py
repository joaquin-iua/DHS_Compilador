from ID import *
from Context import Context

class SymbolsTable():

    _instance = None  
    _contextStack = []  

    def __new__(cls):
        if SymbolsTable._instance is None:
            SymbolsTable._instance = object.__new__(cls)
            SymbolsTable._contextStack.append(Context())  
        return SymbolsTable._instance

    @property
    def contextStack(self):
        return SymbolsTable._contextStack

    def addContext(self):
        SymbolsTable._contextStack.append(Context())

    def deleteContext(self):
        return SymbolsTable._contextStack.pop()

    def getLastContext(self):
        return SymbolsTable._contextStack[-1]

    def findIdGlobal(self, idName) -> Context:
        local_context = SymbolsTable.findIdLocal(self, idName)
        if local_context:
            return local_context

        global_context = SymbolsTable.findId(self, idName)
        if global_context:
            return global_context

        # print(f"Identifier '{idName}' not found")

    def findId(self, idName) -> Context:
        for Context in SymbolsTable._contextStack[-2::-1]:
            if idName in Context.symbols:
                return Context

   
    def findIdLocal(self, idName) -> Context:
        if idName in SymbolsTable._contextStack[-1].symbols:
            return SymbolsTable._contextStack[-1]

    def addId(self, id):
        SymbolsTable._contextStack[-1].addSymbol(id)


