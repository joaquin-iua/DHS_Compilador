grammar compiladores;

fragment LETTER : [A-Za-z] ;
fragment DIGIT : [0-9] ;

EQ : '=' ;
LP : '(' ;
RP : ')' ;
LB : '{' ;
RB : '}' ;
SEMICOLON : ';' ;
COMA : ',' ;

LT: '<';
GT: '>';
EQQ: '==';
NE: '!=';
GE: '>=';
LE: '<=';
AND: '&&';
OR: '||';
PLUS : '+';
MINUS : '-';
MULTIPLICATION : '*';
DIVISION : '/';
MODULE : '%';
INCREMENT : '++';
DECREMENT : '--';

INT : 'int';
DOUBLE:'double' ;

WHILE : 'while' ;
FOR : 'for';
IF : 'if';
ELSE : 'else';
RETURN : 'return';

NUMBER : DIGIT+ ;
ID : (LETTER | '_')(LETTER | DIGIT | '_')* ;
WS : [ \t\r\n] -> skip ;
OTHER : . ;

program : instructions EOF ;

instructions : instruction instructions
              |
              ;

instruction : declaration SEMICOLON
            | assignment SEMICOLON
            | return_stmt SEMICOLON
            | if_stmt
            | for_stmt
            | while_stmt
            | function_prototype SEMICOLON
            | function
            | function_call SEMICOLON
            | block
            ;

declaration : datatype ID definition var_list ;

var_list : COMA ID definition var_list
          |
          ;

definition : EQ arithmetic_logical_op
           |
           ;

assignment : ID EQ arithmetic_logical_op;

datatype  : INT 
          | DOUBLE
          ;

block : LB instructions RB;

if_stmt : IF LP arithmetic_logical_op RP instruction | IF LP arithmetic_logical_op RP instruction else_stmt;

else_stmt : ELSE block;

for_stmt : FOR LP assignment SEMICOLON arithmetic_logical_op SEMICOLON assignment SEMICOLON instruction;

while_stmt : WHILE LP arithmetic_logical_op RP instruction ;

return_stmt : RETURN arithmetic_logical_op;

arithmetic_logical_op : logical_expression;

logical_expression : logical_term logical_exp;

logical_exp : OR logical_term logical_exp
     |;

logical_term : expression lterm | expression cmp expression lterm;

lterm : AND logical_expression lterm
      |;

expression : arithmetic_term exp;

exp : PLUS   arithmetic_term exp
    | MINUS arithmetic_term exp
    |
    ;

arithmetic_term : factor term ;

term : MULTIPLICATION factor term
     | DIVISION  factor term    
     | MODULE  factor term
     |
     ;

factor : ID
       | NUMBER
       | function_call
       | MINUS NUMBER
       | MINUS ID
       | LP logical_expression RP
       ;

function_prototype : datatype ID LP received_args RP;

function : datatype ID LP received_args RP block ;

function_call : ID LP sent_args RP;

received_args : datatype ID received_args_list
              |;

received_args_list : COMA datatype  ID received_args_list
            | ;

sent_args : expression sent_args_list
             |;

sent_args_list: COMA expression sent_args_list
                  |;

cmp : GT 
    | LT
    | EQQ 
    | NE 
    | GE
    | LE
    ;
    