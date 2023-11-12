
# implement with FileManager('name.txt') as name:

class FileManager:

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.name = open(self.name, 'a')
        return self.name

    def __exit__(self, exception_type, exception_value, error_traceback):
        if self.name:
            self.name.close()