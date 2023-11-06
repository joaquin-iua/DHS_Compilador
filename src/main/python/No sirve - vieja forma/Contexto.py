class Contexto:
    def __init__(self):
        self.simbolos = {}

    def agregar_simbolo(self, simbolo):
        if simbolo.nombre in self.simbolos:
            raise Exception(f"Error: El símbolo {simbolo.nombre} ya existe en este contexto.")
        self.simbolos[simbolo.nombre] = simbolo

    def find(self, nombre):
        for contexto in reversed(self.ctx):
            if nombre in contexto.simbolos:
                return contexto.simbolos[nombre]
        return None
