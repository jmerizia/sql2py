grammar Postgresql;


queries
    :  query (';' query)*
    ;

query
    :  create_query
    |  drop_query
    |  select_query
    |  insert_query
    |  delete_query
    |  update_query
    |  empty_query
    ;

create_query
    :  K_CREATE K_TABLE ( K_IF K_NOT K_EXISTS )? table_ref '(' column_defs ')'
    ;

drop_query
    :  K_DROP K_TABLE ID
    ;

select_query
    :  K_SELECT column_refs K_FROM table_ref ( K_WHERE simple_expr )?
    ;

insert_query
    :  K_INSERT K_INTO table_ref '(' column_refs ')' K_VALUES '(' column_values ')' ( K_RETURNING ID )?
    ;

delete_query
    :  K_DELETE K_FROM table_ref ( K_WHERE simple_expr )?
    ;

update_query
    :  K_UPDATE table_ref K_SET column_ref '=' atom ( ',' column_ref '=' atom )* ( K_WHERE simple_expr )?
    ;

empty_query : ;

column_refs
    :  column_ref (',' column_ref)*
    |  '*'
    ;

column_ref
    :  ID
    ;

table_ref
    :  ID
    ;

column_defs
    :  column_def (',' column_def)+
    ;

column_def
    :  ID column_type
    ;

column_values
    :  atom (',' atom)*
    ;

column_type 
    :  ( K_INTEGER | K_TEXT | K_BOOLEAN | K_SERIAL ) ( K_NOT K_NULL )? ( K_PRIMARY K_KEY )?
    ;

// simple non-recursive binary operator expression
simple_expr
    :  atom ( is_eq | gt | lt | K_AND | K_OR | neq ) atom
    ;  

atom
    :  INT
    |  ID
    |  K_FALSE
    |  K_TRUE
    |  qm
    |  STRING
    ;

WS :  [ \t\n\r]+ -> skip ;
K_SELECT : S E L E C T ;
K_DELETE : D E L E T E ;
K_FROM : F R O M ;
K_CREATE : C R E A T E ;
K_TABLE : T A B L E ;
K_INTEGER : I N T E G E R ;
K_TEXT : T E X T ;
K_NOT : N O T ;
K_NULL : N U L L ;
K_IF : I F ;
K_EXISTS : E X I S T S ;
K_SERIAL : S E R I A L ;
K_PRIMARY : P R I M A R Y ;
K_RETURNING : R E T U R N I N G ;
K_BOOLEAN : B O O L E A N ;
K_KEY : K E Y ;
K_DROP : D R O P ;
K_WHERE : W H E R E ;
K_INSERT : I N S E R T ;
K_INTO : I N T O ;
K_VALUES : V A L U E S ;
K_TRUE : T R U E ;
K_FALSE : F A L S E ;
K_UPDATE : U P D A T E ;
K_AND : A N D ;
K_OR : O R ;
K_SET : S E T ;
ID :  [a-zA-Z_]+ ;
INT :  [0-9]+ ;
NEWLINE : '\r'? '\n' ;
is_eq : '==' | '=' ;
neq : '!=' ;
gt : '>' ;
lt : '<' ;
qm : '?' ;
STRING
    :  '\'' (~'\'')* '\''
    |  '"' (~'"')* '"'
    ;


fragment A : [aA];
fragment B : [bB];
fragment C : [cC];
fragment D : [dD];
fragment E : [eE];
fragment F : [fF];
fragment G : [gG];
fragment H : [hH];
fragment I : [iI];
fragment J : [jJ];
fragment K : [kK];
fragment L : [lL];
fragment M : [mM];
fragment N : [nN];
fragment O : [oO];
fragment P : [pP];
fragment Q : [qQ];
fragment R : [rR];
fragment S : [sS];
fragment T : [tT];
fragment U : [uU];
fragment V : [vV];
fragment W : [wW];
fragment X : [xX];
fragment Y : [yY];
fragment Z : [zZ];
