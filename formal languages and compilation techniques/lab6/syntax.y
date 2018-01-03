%{
    #include <string.h>
    #include <stdio.h>
    #include <stdlib.h>

    extern int yylex();
    extern int yyparse();
    extern void update(FILE*);
    extern void print();
    extern FILE *yyin;
    extern FILE *asm_file;
    extern int lineNo;
    void yyerror(const char *s);
%}

%token INTSYM 
%token IFSYM  
%token WHILESYM 
%token ELSESYM 
%token PLUS 
%token MINUS 
%token SLASH 
%token TIMES 
%token LSS 
%token GTR 
%token BECOMES 
%token ACOP 
%token ACCL 
%token SEMICOLON 
%token COMMA
%token LPAREN 
%token RPAREN 
%token AMP
%token MAINFNC 
%token STDIO
%token RTRNSYM 
%token INCDIR
%token CONSTSYM
%token SCANF
%token PRINTF
%token INTFMT

%token IDENT
%token CONSTANT

%%

program: directives INTSYM MAINFNC LPAREN RPAREN ACOP statement_list ACCL
directives: INCDIR LSS STDIO GTR

statement_list: statement | statement statement_list
statement: declaration SEMICOLON | assignment SEMICOLON | if_stmt | output SEMICOLON | input SEMICOLON | RTRNSYM CONSTANT SEMICOLON
block_code: ACOP statement_list ACCL | statement

declaration: 
      INTSYM IDENT 
    | INTSYM IDENT BECOMES CONSTANT 
    | INTSYM IDENT BECOMES expression

assignment: 
      IDENT BECOMES CONSTANT 
    | IDENT BECOMES expression

expression: 
      term 
    | term operator expression 

term: 
      CONSTANT 
    | IDENT

operator: PLUS | MINUS | SLASH | TIMES

if_stmt: 
    IFSYM LPAREN expression RPAREN block_code

input: 
    SCANF LPAREN INTFMT COMMA AMP IDENT RPAREN
output: 
    PRINTF LPAREN INTFMT COMMA IDENT RPAREN

%%

int main(int argc, char *argv[]) {
    ++argv, --argc; /* skip over program name */ 
    
    // sets the input for flex file
    if (argc > 0) 
        yyin = fopen(argv[0], "r"); 
    else 
        yyin = stdin; 
    
    asm_file = fopen("file.asm", "w");
    //read each line from the input file and process it
    while (!feof(yyin)) {
        yyparse();
    }
    update(asm_file);
    //print();
    printf("The file is lexically and sintactly correct!\n");
    return 0;
}

void yyerror(const char *s) {
    printf("Error: %s at line -> %d ! \n", s, lineNo);
    exit(1);
}

