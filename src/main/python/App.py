import sys
from antlr4 import *
from compiladoresLexer  import compiladoresLexer
from compiladoresParser import compiladoresParser
from MyListener import MyListener
from MyVisitor import MyVisitor
from Cleaner import Cleaner
from Optimizer import Optimizer
from ErrorsCounter import ErrorsCounter

def main(argv):
    
    # Limpiamos la carpeta output antes del proceso de compilacion.
    Cleaner.clean_folder("output")
    
    # Comienza el proceso de compilacion.
    inputFile = "input/complete.c"
    outputFile = "output/intermediate_code.txt"
    if len(argv) > 1 :
        inputFile = argv[1]
    input = FileStream(inputFile)
    lexer = compiladoresLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladoresParser(stream)
    
    errorsCounter = ErrorsCounter()
    # errorsCounter.increment()
    
    print("START OF LISTENER".center(80, '-'))
    listener = MyListener()
    parser.addParseListener(listener)
    tree = parser.program()
    print("END OF LISTENER".center(80, '-') + "\n\n")
    
    # print(tree.toStringTree(recog=parser))
    
    # Verificar que no haya errores en el visitor. Luego crear codigo intermedio.
    if(errorsCounter.get_count() == 0):
        print("CONTINUING: No errors found".center(80, '-'))
        print("START OF VISITOR".center(80, '-'))
        visitor = MyVisitor()
        visitor.visit(tree)
        print("END OF VISITOR".center(80, '-'))
    
        # Limpiar el archivo de salida de codigo intermedio.
        Cleaner.clean_file(outputFile)
        
        # Optimizar el archivo de salida de codigo intermedio.
        Optimizer.optimize_intermediate_code(outputFile)
    else:
        print(f'STOPPING: There were found {errorsCounter.get_count()} errors in the program.'.center(80, '-'))
    
if __name__ == '__main__':
    main(sys.argv)