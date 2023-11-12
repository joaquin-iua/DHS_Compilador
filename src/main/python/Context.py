class Context():
    cont = 0

    def __init__(self, **kwargs):
        self._symbols = kwargs
        self.contextNum = Context.cont
        Context._contIncrement()
    
    def __str__(self) -> str:
        output = "-------------------------------------------------------------------------------------\n"
        output += f'\nContext[{self.contextNum}]\n'
        output += "ID\t\t\t\t\t\tNAME\t\t\tDATATYPE\t\tINICIALIZED\t\t\tACCESSED\n"
        for key, value in self._symbols.items():
            output += f"\n{str(value)}\n"
        output += "-------------------------------------------------------------------------------------\n\n\n\n\n"
        return output

    @property
    def symbols(self):
        return self._symbols

    def addSymbol(self, id):
        self._symbols[id.name] = id
    
    @classmethod
    def _contIncrement(cls):
        Context.cont += 1

