import sys
from antlr4 import *
from compiladoresLexer  import compiladoresLexer
from compiladoresParser import compiladoresParser
from MiListener import MiListener

def main(argv):
    archivo = "input/decl.c"
    if len(argv) > 1:
        archivo = argv[1]

    # Crear un flujo de entrada a partir del archivo fuente
    input = FileStream(archivo)

    # Crear un lexer y un flujo de tokens a partir del flujo de entrada
    lexer = compiladoresLexer(input)
    stream = CommonTokenStream(lexer)

    # Crear un parser a partir del flujo de tokens
    parser = compiladoresParser(stream)

    # Crear una instancia de tu clase personalizada MiListener
    listener = MiListener("output/Tabla_De_Simbolos.txt")

    # Agregar el listener al parser
    parser.addParseListener(listener)

    # Iniciar el análisis sintáctico llamando a la regla 'program' (raíz de la gramática)
    tree = parser.program()

    # En este punto, el análisis sintáctico ha finalizado y el listener ha recopilado la información necesaria.

    # dibujar el arbol
    #print("************************************************************************")
    #print("ARBOL GENERADO")
    #print(tree.toStringTree(recog=parser))


if __name__ == '__main__':
    main(sys.argv)
