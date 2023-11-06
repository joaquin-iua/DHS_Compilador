grammar compiladores;

// Tokens
fragment LETTER: [A-Za-z];
fragment DIGIT: [0-9];

EQ: '='; // Token para el operador de asignación
EQQ: '=='; // Token para el operador de igualdad
NE: '!='; // Token para el operador de desigualdad
LT: '<'; // Token para el operador menor que
GT: '>'; // Token para el operador mayor que
LE: '<='; // Token para el operador menor o igual que
GE: '>='; // Token para el operador mayor o igual que
PP: '++'; // Token para el operador de incremento
MM: '--'; // Token para el operador de decremento
PLUS: '+'; // Token para el operador de suma
MINUS: '-'; // Token para el operador de resta
MULT: '*'; // Token para el operador de multiplicación
DIV: '/'; // Token para el operador de división
MOD: '%'; // Token para el operador de módulo
AND: '&&'; // Token para el operador lógico AND
OR: '||'; // Token para el operador lógico OR
NOT: '!'; // Token para el operador lógico NOT
LPAREN: '('; // Token para paréntesis izquierdo
RPAREN: ')'; // Token para paréntesis derecho
LBRACE: '{'; // Token para llave izquierda
RBRACE: '}'; // Token para llave derecha
SEMICOLON: ';'; // Token para punto y coma
COMMA: ','; // Token para coma

NUM: DIGIT+; // Token para números enteros
INT: 'int'; // Token para la palabra clave 'int'
DOUBLE: 'double'; // Token para la palabra clave 'double'
WHILE: 'while'; // Token para la palabra clave 'while'
IF: 'if'; // Token para la palabra clave 'if'
FOR: 'for'; // Token para la palabra clave 'for'
RETURN: 'return'; // Token para la palabra clave 'return'
ID: (LETTER | '_') (LETTER | DIGIT | '_')*; // Token para identificadores

WS:
	[ \t\n\r] -> skip; // Token para espacios en blanco (ignorado)
OTHER: .; // Token para cualquier otro carácter

program: instructions EOF; // Regla inicial del programa

instructions:
	instruction instructions
	|; // Regla para instrucciones

instruction:
	declaration SEMICOLON // Regla para declaraciones
	| assignment SEMICOLON // Regla para asignaciones
	| return_statement SEMICOLON // Regla para declaraciones de retorno
	| if_statement // Regla para declaraciones condicionales
	| for_statement // Regla para declaraciones de bucle 'for'
	| while_statement // Regla para declaraciones de bucle 'while'
	| block // Regla para bloques de código
	| function_prototype // Regla para prototipado de funciones.
	| function_call // Regla para llamado a funciones.
	| function_definition; // Regla para definiciones de funciones
	
declaration:
	datatype ID definition variable_list; // Regla para declaraciones de variables

definition:
	EQ NUM
	|; // Regla para definiciones de variables (opcional)

variable_list:
	COMMA ID definition variable_list
	|; // Regla para listas de variables

block:
	LBRACE instructions RBRACE; // Regla para bloques de código

return_statement:
	RETURN expression; // Regla para declaraciones de retorno

if_statement:
	IF LPAREN logical_expression RPAREN instruction else_statement;
	// Regla para declaraciones condicionales

else_statement:
	'else' instruction
	|; // Regla para el bloque 'else' (opcional)

for_statement:
	FOR LPAREN assignment SEMICOLON logical_expression SEMICOLON assignment RPAREN instruction;
	// Regla para declaraciones de bucle 'for'

while_statement:
	WHILE LPAREN logical_expression RPAREN instruction; // Regla para declaraciones de bucle 'while'

assignment:
	ID EQ arithmetic_operation // Regla para asignaciones aritméticas
	| ID EQ function_call // Regla para asignaciones de llamadas a funciones
	| ID EQ logical_operation // Regla para asignaciones lógicas
	| ID PLUS PLUS // Regla para incremento
	| ID MINUS MINUS; // Regla para decremento

arithmetic_operation:
	expression; // Regla para operaciones aritméticas

logical_operation:
	logical_expression; // Regla para operaciones lógicas

expression: term additive_expression |; // Regla para expresiones

additive_expression:
	PLUS term additive_expression
	| MINUS term additive_expression
	|; // Regla para expresiones aritméticas

term: factor multiplicative_expression |; // Regla para términos

multiplicative_expression:
	MULT factor multiplicative_expression
	| DIV factor multiplicative_expression
	| MOD factor multiplicative_expression
	|; // Regla para expresiones multiplicativas

factor:
	negative_sign NUM // Regla para números negativos
	| negative_sign ID // Regla para identificadores negativos
	| function_call // Regla para llamadas a funciones
	| LPAREN expression RPAREN; // Regla para expresiones entre paréntesis

negative_sign: MINUS |; // Regla para signo negativo (opcional)

logical_expression:
	logical_term logical_expression_; // Regla para expresiones lógicas

logical_expression_:
	OR logical_term logical_expression_
	|; // Regla para operaciones lógicas OR

logical_term:
	logical_factor logical_term_; // Regla para términos lógicos

logical_term_:
	AND logical_factor logical_term_
	|; // Regla para operaciones lógicas AND

logical_factor:
	factor // Regla para factores lógicos
	| comparison // Regla para comparaciones
	| LPAREN logical_expression RPAREN; // Regla para expresiones lógicas entre paréntesis

comparison:
	arithmetic_operation comparison_operator arithmetic_operation
	| comparison comparison_operator comparison; // Regla para comparaciones

comparison_operator:
	EQQ
	| NE
	| GT
	| LT
	| GE
	| LE; // Regla para operadores de comparación

datatype:
	DOUBLE
	| INT; // Regla para tipos de datos (double o int)

// Manejo de Funciones.

// Prototipo de Función.
function_prototype:
	datatype ID LPAREN parameters RPAREN SEMICOLON; // Regla para prototipos de funciones

parameters:
	datatype ID parameters_list
	|; // Regla para parámetros de funciones (opcional)

parameters_list:
	COMMA datatype ID parameters_list
	|; // Regla para listas de parámetros de funciones (opcional)

// Definición de Función.
function_definition:
	datatype ID LPAREN parameters RPAREN block; // Regla para definiciones de funciones

// Llamada a Función.
function_call:
	ID LPAREN arguments RPAREN; // Regla para llamadas a funciones

arguments:
	expression arguments_list
	|; // Regla para argumentos de funciones (opcional)

arguments_list:
	COMMA expression arguments_list
	|; // Regla para listas de argumentos de funciones (opcional)