// FECHAPAR : ('0'[1-9] | [12] DIGITO | '30') '/' ('0'[2468] | '1'[02]) '/' DIGITO DIGITO DIGITO
// DIGITO ;

// s : ID {print("ID ->" + $ID.text + "<--") } s | NUMERO {print("NUMERO ->" + $NUMERO.text + "<--")
// } s | OTRO {print("Otro ->" + $OTRO.text + "<--") } s | HORAPAR {print("Hora par ->" +
// $HORAPAR.text + "<--") } s | FECHAPAR {print("Mes par ->" + $FECHAPAR.text + "<--") } s | EOF ;

// si : s EOF ;

// s : PA s PC s | ;


// PREGUNTAR PROBLEMA CON EL BUCLE FOR AL LEER 
/*
for (int i = 0; i < 5; i = 1 + 1) {
    i = 3 + 1;
}

AL LEERLO RECONOCE TODO BIEN PERO EXIGE UN ; DESPUES DEL ) Y ANTES DE LA {
*/
grammar compiladores;

// Tokens para letras y dígitos
fragment LETRA:
	[A-Za-z]; // Representa una letra (mayúscula o minúscula)
fragment DIGITO: [0-9]; // Representa un dígito del 0 al 9

// Tokens para símbolos comunes
EQ: '='; // Representa el operador de asignación
PA: '('; // Representa el paréntesis de apertura
PC: ')'; // Representa el paréntesis de cierre
LLA: '{'; // Representa la llave de apertura
LLC: '}'; // Representa la llave de cierre
PYC: ';'; // Representa el punto y coma
COMA: ','; // Representa la coma

// Token para números
NUMERO:
	DIGITO+; // Representa un número compuesto por uno o más dígitos

// Tokens para tipos de datos y palabras clave
TDATO:
	'int'
	| 'double'; // Representa tipos de datos como 'int' o 'double'
WHILE: 'while'; // Representa la palabra clave 'while'

// Token para identificadores
ID: (LETRA | '_') (LETRA | DIGITO | '_')*;
// Representa un identificador que comienza con una letra o guión bajo, seguido de letras, dígitos o guiones bajos adicionales

// Token para espacios en blanco, tabulaciones y saltos de línea (omitido en el análisis)
WS: [ \t\r\n]+ -> skip;
// Modificado para incluir el '+' después del conjunto de caracteres en blanco

// Token para cualquier otro carácter (usado para manejar caracteres no reconocidos)
OTRO: .;

// Regla Inicial de la Gramatica. Un programa: Un programa se compone de instrucciones y termina con
// el final del archivo (EOF).
programa: instrucciones EOF;

// Conjunto de Instrucciones: Conjunto de instrucciones, puede estar vacío.
instrucciones: instruccion instrucciones |;

// Una instrucción: Puede ser una declaración, asignación, retorno, condicional if, bucle for, bucle while o bloque de código.
instruccion:
	declaracion
	| asignacion
	| retornar
	| if_stmt
	| for_stmt
	| while_stmt
	| bloque;

// Una declaración: Define una variable con un tipo de dato, un identificador, una definición y una lista de variables.
declaracion: TDATO ID definicion lista_var PYC;

// Una lista de variables al realizar una declaración: Puede ser una lista de variables separadas por comas o estar vacía.
lista_var: COMA ID definicion lista_var |;

// Una asignación: Asigna un valor a una variable / opcional para el caso del for el punto y coma.
asignacion: ID EQ opal PYC? PC?;

// Una definición: Puede ser una asignación con un número o estar vacía.
definicion: EQ NUMERO |;

// Nueva regla para expresiones relacionales
relacional: opal ( '>' | '<' | '>=' | '<=' | '==' | '!=') opal;

// Regla if_stmt Representa una estructura de control if, con posibilidad de tener un bloque else.
// Actualizada para usar expresiones relacionales
if_stmt:
	'if' PA relacional PC instruccion ('else' instruccion)?;

// Un bucle for: Representa una estructura de control for.
for_stmt: 'for' PA declaracion_for relacional PYC asignacion PYC instruccion;

// Regla adicional para manejar la declaración de la variable en el bucle for
declaracion_for: TDATO ID definicion PYC;

// Un bucle while: Representa una estructura de control while.
while_stmt: WHILE PA relacional PC instruccion;

// Un bloque de código: Un bloque de código encerrado entre llaves.
bloque: LLA instrucciones LLC;

// La regla retornar (return) para funciones: Representa una declaración de retorno.
retornar: 'return' opal PYC;

// Definición completa de la regla opal: Define las operaciones aritméticas y lógicas.
opal:
	opal '+' opal // Suma
	| opal '-' opal // Resta
	| opal '*' opal // Multiplicación
	| opal '/' opal // División
	| ID // Identificador
	| NUMERO // Número
	| PA opal PC // Paréntesis para agrupar
	| 'true' // Valor booleano verdadero
	| 'false' // Valor booleano falso
	| '!' opal // Negación lógica
	| opal '&&' opal // Operación lógica AND
	| opal '||' opal; // Operación lógica OR