from Contexto import Contexto

class TS:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TS, cls).__new__(cls)
            cls._instance.ctx = [Contexto()]
        return cls._instance

    def agregar_contexto(self):
        self.ctx.append(Contexto())

    def borrar_contexto(self):
        if len(self.ctx) > 1:
            self.ctx.pop()

    def buscar(self, nombre):
        for contexto in reversed(self.ctx):
            if nombre in contexto.simbolos:
                return contexto.simbolos[nombre]
        return None

    def agregar(self, simbolo):
        self.ctx[-1].agregar_simbolo(simbolo)