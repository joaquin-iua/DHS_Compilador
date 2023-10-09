grammar compiladores;

fragment LETRA: [A-Za-z];
fragment DIGITO: [0-9];

EQ: '=';
PA: '(';
PC: ')';
LLA: '{';
LLC: '}';
PYC: ';';
COMA: ',';
MAS: '+';
MENOS: '-';
MULT: '*';
DIV: '/';
MOD: '%';

NUMERO: DIGITO+;

TDATO: 'int' | 'double';
WHILE: 'while';

ID: (LETRA | '_') (LETRA | DIGITO | '_')*;

WS: [ \t\r\n] -> skip;
OTRO: .;

programa: instrucciones EOF;

instrucciones: instruccion instrucciones |;

instruccion:
	declaracion
	| asignacion PYC
	| retornar
	| if_stmt
	| for_stmt
	| while_stmt
	| bloque;

declaracion: TDATO ID definicion lista_var PYC;

definicion: EQ NUMERO |;

bloque: LLA instrucciones LLC;

lista_var: COMA ID definicion lista_var |;

retornar: 'return' opal;

if_stmt: 'if' PA opal PC instruccion else_stmt;

else_stmt: 'else' instruccion |;

for_stmt:
	'for' PA asignacion PYC opal PYC asignacion PC instruccion;

while_stmt: WHILE PA opal PC instruccion;

asignacion: ID EQ opal;

opal: expresion;

expresion: termino exp;

exp: MAS termino exp | MENOS termino exp |;

termino: factor term;

term: MULT factor term | DIV factor term | MOD factor term |;

factor:
	NUMERO
	| ID
	| MENOS NUMERO
	| MENOS ID
	| funcion
	| PA expresion PC;

funcion: ID PA ID PC;