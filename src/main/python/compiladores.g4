grammar compiladores;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

PA: '(' ;
PC: ')' ;

NUMERO : DIGITO+ ;

WS : [ \t\r\n] -> skip ;

OTRO : . ;

ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;

/*s : ID     {print("ID ->" + $ID.text + "<--") }         s
  | NUMERO {print("NUMERO ->" + $NUMERO.text + "<--") } s
  | OTRO   {print("Otro ->" + $OTRO.text + "<--") }     s
  | EOF
  ;*/

/* 
// Regla Gramatical
si: s EOF ;

// Regla Sintactica
s : PA s PC s
  | 
  ;
*/


