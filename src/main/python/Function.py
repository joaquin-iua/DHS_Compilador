from ID import ID

class Function(ID):
    def __init__(self, nombre, tdato):
        super().__init__(nombre, tdato)
        self.args = []

    def add_argument(self, argument):
        self.args.append(argument)
