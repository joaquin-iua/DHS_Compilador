from abc import ABC, abstractmethod

class ID(ABC):

    def __init__(self, name, datatype, inicialized=False, accessed=False):
        self._name = name
        self._datatype = datatype
        self._inicialized = inicialized
        self._accessed = accessed

    def __str__(self) -> str:
        return f'{self.__class__.__name__}\t\t\t\t{self._name}\t\t\t\t{self._datatype}\t\t\t\t{self._inicialized}\t\t\t\t{self._accessed}'

    def __eq__(self, other) -> bool:
        if isinstance(other, ID):
            return other.name == self.name and other.datatype == self.datatype

    @property
    def name(self):
        return self._name

    @property
    def datatype(self):
        return self._datatype

    @property
    def inicialized(self):
        return self._inicialized
    
    def setInitialized(self):
        self._inicialized = True

    @property
    def accessed(self):
        return self._accessed
    
    def setAccessed(self):
        self._accessed = True

    @name.setter
    def name(self, name):
        self._name = name

    @datatype.setter
    def datatype(self, datatype):
        self._datatype = datatype

    @inicialized.setter
    def inicialized(self, flag):
        self._inicialized = flag

    @accessed.setter
    def accessed(self, flag):
        self._accessed = flag


class Variable(ID):
    pass


class Function(ID):

    def __init__(self, name, datatype, args, inicialized=False, accessed=False):
        super().__init__(name, datatype, inicialized, accessed)
        self._args = list(args)

    def __str__(self) -> str:
        output = ""
        for i in self._args:
            output += f'{str(i)}\n' 
        return f'{super().__str__()}\nargs:[\n{output}]'

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and other.args == self.args

    @property
    def args(self):
        return self._args