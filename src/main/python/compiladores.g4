grammar compiladores;

PALABRA_MAYUSCULA : [A-Z][a-zA-Z0-9_]* ;
NUMERO_PAR : [02468]+ ;
FECHA_PAR : '[0-9]{2}-[0-9]{2}-[0-9]{4}' ;
HORA_PAR : '11:' [4-5][0-9] | '12:' [0-5][0-9] | '13:' [0-5][0-9] | '14:' [0-1][0-5] ;
HEXADECIMAL : '0x'[0-9a-fA-F]+ ;

s : PALABRA_MAYUSCULA {print("PALABRA_MAYUSCULA ->" + $PALABRA_MAYUSCULA.text + "<--") } s
  | NUMERO_PAR {print("NUMERO_PAR ->" + $NUMERO_PAR.text + "<--") } s
  | FECHA_PAR {print("FECHA_PAR ->" + $FECHA_PAR.text + "<--") } s
  | HORA_PAR {print("HORA_PAR ->" + $HORA_PAR.text + "<--") } s
  | HEXADECIMAL {print("HEXADECIMAL ->" + $HEXADECIMAL.text + "<--") } s
  | EOF
  ;