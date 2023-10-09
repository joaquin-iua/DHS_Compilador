import sys
from antlr4 import *
from compiladoresLexer  import compiladoresLexer
from compiladoresParser import compiladoresParser


def main(argv):
    archivo = "input/decl.c" # cambiar
    if len(argv) > 1 :
        archivo = argv[1]
    input = FileStream(archivo)
    lexer = compiladoresLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladoresParser(stream)
    tree = parser.programa() # cambiar
    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)