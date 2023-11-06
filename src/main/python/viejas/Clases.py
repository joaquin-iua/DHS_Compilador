class Contexto:
    def __init__(self):
        self.simbolos = {}

class ID:
    def __init__(self, nombre, tdato):
        self.nombre = nombre
        self.tdato = tdato
        self.inicializado = False
        self.accedido = False

class Funcion(ID):
    def __init__(self, nombre, tdato, args):
        super().__init__(nombre, tdato)
        self.args = args

class Variable(ID):
    def __init__(self, nombre, tdato):
        super().__init__(nombre, tdato)

class TS:
    def __init__(self):
        self.ctx = [Contexto()]

    def buscarLocal(self, nombre):
        if nombre in self.ctx[-1].simbolos:
            return self.ctx[-1].simbolos[nombre]
        return None

    def buscar(self, nombre):
        for contexto in reversed(self.ctx):
            if nombre in contexto.simbolos:
                return contexto.simbolos[nombre]
        return None

    def agregar(self, id):
        if id.nombre in self.ctx[-1].simbolos:
            raise ValueError(f"Error: El identificador '{id.nombre}' ya ha sido declarado en este contexto.")
        self.ctx[-1].simbolos[id.nombre] = id

    def agregarContexto(self):
        self.ctx.append(Contexto())

    def borrarContexto(self):
        if len(self.ctx) > 1:
            self.ctx.pop()
        else:
            raise ValueError("Error: No se puede eliminar el contexto global.")

# Ejemplo de uso:
ts = TS()
ts.agregarContexto()
variable_x = Variable("x", "int")
ts.agregar(variable_x)
print(ts.buscar("x"))  # Debería imprimir: <Variable object at ...>
ts.borrarContexto()
