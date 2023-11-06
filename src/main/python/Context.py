from ID import ID

class Context:
    def __init__(self):
        self.ids = {}

    def add_id(self, id):
        if self.ids.get(id.name) != None:
            raise Exception(f"Error: El símbolo {id.nombre} ya existe en este contexto.")
        self.ids[id.name] = id

    def find(self, name):
        if name in self.ids.keys():
            return self.ids.get(name)
            
        return None
    
    def to_string(self):
        for id in self.ids.values():
            return f"nombre: {id.name}, datatype: {id.datatype}"
