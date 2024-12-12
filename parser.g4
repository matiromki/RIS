parser grammar ExprParser;
options { tokenVocab=ExprLexer; }

game: rules+;

rules
    : includeRule
    | canRule
    | canControlRule
    | predatesRule
    | mustRule
    | haveRule
    | launchRule
    ;

includeRule : ID INCLUDE list_id;

canRule : list_id CAN list_id;

canControlRule: ID CAN_CONTROL list_id;

predatesRule : ID PREDATES ID;

mustRule : ID MUST ID WHILE ID;

haveRule : ID HAVE HP;

launchRule : ID LAUNCH ID;


list_id: ID (COMMA ID)* ;
