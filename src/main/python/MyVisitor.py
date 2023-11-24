from compiladoresParser import compiladoresParser
from compiladoresVisitor import compiladoresVisitor
from FileManager import *
from Temps import *

class MyVisitor(compiladoresVisitor):
    def __init__(self):
        self.params = []
        # Clear the content of the file initially
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.truncate(0)
    
    tmp = Temps()

    def visitProgram(self, ctx: compiladoresParser.ProgramContext):
        print("Visiting Program".center(80, '*'))
        return self.visitChildren(ctx)

    def visitDeclaration(self, ctx: compiladoresParser.DeclarationContext):
        print("Visiting Declaration".center(80, '*'))
        self.visitDefinition(ctx.getChild(2))
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write('\n' + ctx.getChild(1).getText() +
                          ' = ' + self.tmp.currentT)

    def visitDefinition(self, ctx: compiladoresParser.DefinitionContext):
        if ctx.getChildCount() > 1:
            return self.visitArithmetic_logical_op(ctx.getChild(1))
        else:
            print("This declaration is without a valued definition.".center(80, '-'))

    def visitAssignment(self, ctx: compiladoresParser.AssignmentContext):
        print("Visiting Assignment".center(80, '*'))
        self.visitArithmetic_logical_op(ctx.getChild(2))
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write('\n' + ctx.getChild(0).getText() +
                          ' = ' + self.tmp.currentT)

    def visitArithmetic_logical_op(self, ctx: compiladoresParser.Arithmetic_logical_opContext):
        return self.visitLogical_expression(ctx.getChild(0))

    def visitLogical_expression(self, ctx: compiladoresParser.Logical_expressionContext):
        return self.visitLogical_term(ctx.getChild(0))

    def visitLogical_exp(self, ctx: compiladoresParser.Logical_expContext):
        return self.visitChildren(ctx)

    def visitLogical_term(self, ctx: compiladoresParser.Logical_termContext):
        return self.visitExpression(ctx.getChild(0))

    def visitLterm(self, ctx: compiladoresParser.LtermContext):
        return self.visitChildren(ctx)

    def visitFactor(self, ctx: compiladoresParser.FactorContext):
        if ctx.getChild(0).getText() == '(':
            return self.visitLogical_expression(ctx.getChild(1))
        return self.visitChild(0).getText()

    def visitExpression(self, ctx: compiladoresParser.ExpressionContext):
        print("Visiting Expression".center(80, '*'))

        aux = self.visitArithmetic_term(ctx.getChild(0))
        if ctx.getChild(1).getText() != '':
            aux2 = self.visitExp(ctx.getChild(1))
            with FileManager("output/intermediate_code.txt") as ICFile:
                ICFile.write('\n' + self.tmp.t + ' = ' + aux + ' ' +
                              ctx.getChild(1).getChild(0).getText() + ' ' + aux2)
        return self.tmp.currentT

    def visitExp(self, ctx: compiladoresParser.ExpContext):
        print("Visiting Expression".center(80, '*'))

        aux1 = self.visitArithmetic_term(ctx.getChild(1))

        # Base case for recursion
        # If the child 3 is empty, recursion ends
        if ctx.getChild(2).getText() == '':
            return self.tmp.currentT

        # Record in the file the addition or subtraction of Temps corresponding to each Expression
        aux = self.visitExp(ctx.getChild(2))
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write('\n' + self.tmp.t + ' = ' + aux1 +
                          ' ' + ctx.getChild(2).getChild(0).getText() + ' ' + aux)
        return self.tmp.currentT

    def visitArithmetic_term(self, ctx: compiladoresParser.Arithmetic_termContext):
        print("Visiting Arithmetic Term".center(80, '*'))
        # Check if the factor is an Expression enclosed in parentheses
        if ctx.getChild(0).getChild(0).getText() == '(':
            b = self.visitFactor(ctx.getChild(0))
            if ctx.getChild(1).getText() != '':
                a = self.visitTerm(ctx.getChild(1))
                with FileManager("output/intermediate_code.txt") as ICFile:
                    ICFile.write('\n' + self.tmp.t + ' = ' + b + ' ' +
                                  ctx.getChild(1).getChild(0).getText() + ' ' + a)

        else:
            with FileManager("output/intermediate_code.txt") as ICFile:
                ICFile.write('\n' + self.tmp.t + ' = ' +
                              str(ctx.getChild(0).getText()))
            if ctx.getChild(1).getText() != '':
                return self.visitTerm(ctx.getChild(1))
        return self.tmp.currentT

    def visitTerm(self, ctx: compiladoresParser.TermContext):
        # Check if the factor is an Expression enclosed in parentheses
        if ctx.getChild(1).getChild(0).getText() == '(':
            self.visitFactor(ctx.getChild(1))

        # If not, create a temporary and perform the operation of the previous temporary and the new number
        # Record in the file t_new = t_previous + value
        else:
            with FileManager("output/intermediate_code.txt") as ICFile:
                ICFile.write('\n' + self.tmp.t + ' = ' + self.tmp.previousT +
                              ' ' + ctx.getChild(0).getText() + ' ' + ctx.getChild(1).getText())
        # Base case for recursion
        # If the child 3 is empty, recursion ends
        if ctx.getChild(2).getText() == '':
            return self.tmp.currentT
        return self.visitTerm(ctx.getChild(2))
    
        
    def visitWhile_stmt(self, ctx: compiladoresParser.While_stmtContext):
        print("Visiting While Statement".center(80, '*'))

        # Etiqueta de inicio del bucle while
        start_label = self.tmp.t
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\nlabel {start_label}\n')

        # Generar código para la condición del bucle
        condition_label = self.tmp.t
        loop_end_label = self.tmp.t  # Etiqueta diferente para el final del bucle

        # Realizar la asignación t3 = condicion
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'{condition_label} = ' + ctx.getChild(2).getText() + '\n')
            
        self.visitArithmetic_logical_op(ctx.getChild(2))
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\nifn {condition_label}jmp {loop_end_label}\n')

        # Generar código para el cuerpo del bucle
        self.visitInstruction(ctx.getChild(4))

        # Volver a la etiqueta de condición
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\njmp {start_label}\n')

        # Etiqueta de salida del bucle
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\nlabel {loop_end_label}\n')

        return None
    
    
    def visitFor_stmt(self, ctx: compiladoresParser.For_stmtContext):
        print("Visiting For Statement".center(80, '*'))

        # Obtener las asignaciones y condiciones del bucle for
        initialization = ctx.getChild(2).getText()  # Asignación inicial
        condition = ctx.getChild(4).getText()  # Condición
        update = ctx.getChild(6).getText()  # Actualización

        # Etiqueta de inicio del bucle for
        start_label = self.tmp.t
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\n{initialization}\nlabel {start_label}\n')

        # Generar código para la condición del bucle
        condition_label = self.tmp.t
        loop_end_label = self.tmp.t  # Etiqueta diferente para el final del bucle

        # Realizar la asignación de la condición
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'{condition_label} = {condition}\n')

        # Evaluar la condición
        self.visitArithmetic_logical_op(ctx.getChild(4))
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\nifn {condition_label}jmp {loop_end_label}\n')

        # Generar código para el cuerpo del bucle si no es None
        if ctx.getChild(8) is not None:
            self.visitInstruction(ctx.getChild(8))

        # Actualizar la variable de control del bucle
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\n{update}')

        # Volver a la etiqueta de condición
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\njmp {start_label}\n')

        # Etiqueta de salida del bucle
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\nlabel {loop_end_label}\n')

        return None
    
    def visitIf_stmt(self, ctx: compiladoresParser.If_stmtContext):
        print("Visiting If Statement".center(80, '*'))

        # Generar código para la condición del if
        condition_label = self.tmp.t
        else_label = self.tmp.t
        end_if_label = self.tmp.t  # Nueva etiqueta para el final del if
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\n{condition_label} = {ctx.getChild(2).getText()}\n')
            self.visitArithmetic_logical_op(ctx.getChild(2))
            ICFile.write(f'\nifn {condition_label}jmp {else_label}\n')

        # Generar código para el cuerpo del if
        self.visitInstruction(ctx.getChild(4))

        # Saltar al final del if (antes del else)
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\njmp {end_if_label}\n')

        # Generar código para el else (si existe)
        else_label = self.visitElse_stmt(ctx.getChild(5), else_label)

        # Etiqueta de salida del if-else
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\nlabel {end_if_label}\n')

        return None

    def visitElse_stmt(self, ctx: compiladoresParser.Else_stmtContext, else_label):
        if ctx.getChild(1) is not None:  # Verificar si hay un bloque 'else'
            with FileManager("output/intermediate_code.txt") as ICFile:
                ICFile.write(f'\nlabel {else_label}\n')
            
            # Generar código para el cuerpo del 'else'
            self.visitInstruction(ctx.getChild(1))
            
            return else_label
    
    def visitFunction(self, ctx: compiladoresParser.FunctionContext):
        print("Visiting Function Definition".center(80, '*'))

        # Obtener información sobre la función
        function_name = ctx.getChild(1).getText()  # Nombre de la función
        return_type = ctx.getChild(0).getText()  # Tipo de retorno

        # Etiqueta de inicio de la función
        start_label = function_name
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\nlabel {start_label}\n')
            
        # Obtener de vuelta PC
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\npop return_pc\n')

        # Generar código para los argumentos
        self.visitReceived_args(ctx.getChild(3))

        # Generar código para el bloque de la función
        self.visitBlock(ctx.getChild(5))

        # Guardar el valor de retorno de la funcion.
        registro_resultado = self.tmp.currentT
        return_code = f'\npush {registro_resultado}\n'
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(return_code)
            
        # Volver a la ejecucion del programa principal
        with FileManager("output/intermediate_code.txt") as ICFile:   
            ICFile.write(f'\njmp return_pc\n') 
            
        # Etiqueta de salida de la función
        end_function_label = "end_" + function_name
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\nlabel {end_function_label}\n')

        return None
    
    def visitReceived_args(self, ctx: compiladoresParser.Received_argsContext):
        if ctx.getChildCount() > 0:
            # Obtener información sobre el argumento
            arg_type = ctx.getChild(0).getText()
            arg_name = ctx.getChild(1).getText()

            # Realizar operaciones necesarias con los argumentos, por ejemplo, push en la pila
            push_code = f'\npush {arg_name}\n'
            self.params.append((arg_name))
            with FileManager("output/intermediate_code.txt") as ICFile:
                ICFile.write(push_code)

            # Llamar a la función recursivamente para procesar otros argumentos
            self.visitReceived_args_list(ctx.getChild(2))

    def visitReceived_args_list(self, ctx: compiladoresParser.Received_args_listContext):
        if ctx.getChildCount() > 0:
            # Obtener información sobre el argumento
            arg_type = ctx.getChild(1).getText()
            arg_name = ctx.getChild(2).getText()

            # Realizar operaciones necesarias con los argumentos, por ejemplo, push en la pila
            push_code = f'\npush {arg_name}\n'
            self.params.append((arg_name))
            with FileManager("output/intermediate_code.txt") as ICFile:
                ICFile.write(push_code)

            # Llamar a la función recursivamente para procesar otros argumentos
            self.visitReceived_args_list(ctx.getChild(3))
            
    def visitFunction_call(self, ctx: compiladoresParser.Function_callContext):
        print("Visiting Function Call".center(80, '*'))

        # Obtener información sobre la llamada a la función
        function_name = ctx.getChild(0).getText()  # Nombre de la función

        # Generar código para los argumentos de la llamada a la función
        self.visitSent_args(ctx.getChild(2))
        
        # Guardar PC en pila.
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\npush pc + 8\n')

        # Saltar a la funcion.
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\njmp {function_name}\n')
            
        # Obtiene el resultado de la funcion.
        with FileManager("output/intermediate_code.txt") as ICFile:
            ICFile.write(f'\npop function_result\n')

        # Restaurar valores de la pila.
        with FileManager("output/intermediate_code.txt") as ICFile:
            for param in reversed(self.params):
                ICFile.write(f'\npop {param}\n')
                
        return None

    def visitSent_args(self, ctx: compiladoresParser.Sent_argsContext):
        if ctx.getChildCount() > 0:
            # Generar código para el primer argumento
            self.visitExpression(ctx.getChild(0))

            # Llamar a la función recursivamente para procesar otros argumentos
            self.visitSent_args_list(ctx.getChild(1))

    def visitSent_args_list(self, ctx: compiladoresParser.Sent_args_listContext):
        if ctx.getChildCount() > 0:
            # Generar código para el siguiente argumento
            self.visitExpression(ctx.getChild(1))

            # Llamar a la función recursivamente para procesar otros argumentos
            self.visitSent_args_list(ctx.getChild(2))
