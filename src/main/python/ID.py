class ID:
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype
        self.initialized = False
        self.accessed = False
        self.context = None
