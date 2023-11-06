from ID import ID

class Funcion(ID):
    def __init__(self, nombre, tdato):
        super().__init__(nombre, tdato)
        self.args = []

    def agregar_argumento(self, argumento):
        self.args.append(argumento)
