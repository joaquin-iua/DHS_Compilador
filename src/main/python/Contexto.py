class Contexto:
    def __init__(self):
        self.simbolos = {}

    def agregar_simbolo(self, simbolo):
        if simbolo.nombre in self.simbolos:
            raise Exception(f"Error: El símbolo {simbolo.nombre} ya existe en este contexto.")
        self.simbolos[simbolo.nombre] = simbolo
