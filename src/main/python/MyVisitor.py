from compiladoresParser import compiladoresParser
from compiladoresVisitor import compiladoresVisitor
from FileManager import *
from Temps import *


class MyVisitor(compiladoresVisitor):

    def __init__(self):
        super().__init__()
        