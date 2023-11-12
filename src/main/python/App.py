import sys
from antlr4 import *
from compiladoresLexer  import compiladoresLexer
from compiladoresParser import compiladoresParser
from MyListener import MyListener
# from MyVisitor import MyVisitor

def main(argv):
    file = "input/decl.c"
    if len(argv) > 1 :
        file = argv[1]
    input = FileStream(file)
    lexer = compiladoresLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladoresParser(stream)
    listener = MyListener()
    parser.addParseListener(listener)
    tree = parser.program()
    print(tree.toStringTree(recog=parser))
    # visitante = miVisitor()
    # visitante.visit(tree)

if __name__ == '__main__':
    main(sys.argv)