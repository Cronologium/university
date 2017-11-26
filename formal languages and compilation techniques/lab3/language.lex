%{
#define UNKNOWN -1
#define IDENT 0
#define CONSTANT 1
#define INTSYM 2
#define FLOAT 3
#define CHARSYM 4
#define INCMD 5
#define OUTCMD 6
#define IFSYM 7 
#define WHILESYM 8
#define ELSESYM 9
#define PLUS 10
#define MINUS 11
#define SLASH 12
#define TIMES 13
#define LSS 14
#define GTR 15
#define LEQ 16
#define GEQ 17
#define BECOMES 18
#define EQ 19
#define ACOP 20
#define ACCL 21
#define SEMICOLON 22
#define PERIOD 23
#define LPAREN 24
#define RPAREN 25
#define INSTR 26
#define OUTSTR 27
#define STRUCT 28
#define MAINFNC 29
#define IOSTR 30
#define RTRMSYM 31
#define INCDIR 32
#define USINGSYM 33
#define NMSSYN 34
#define STDSYM 35
#define CONSTSYM 36


%}

digit [0-9]
letter [a-fA-F]

%%
"int"                { addPIF( INTSYM, 0);     }
"float"              { addPIF( FLOAT, 0);      }
"char"               { addPIF( CHARSYM, 0);    }
"cin"                { addPIF( INCMD, 0);      }
"cout"               { addPIF( OUTCMD, 0);     }
"if"                 { addPIF( IFSYM, 0);      }
"while"              { addPIF( WHILESYM, 0);   }
"else"               { addPIF( ELSESYM, 0);    }
"+"                  { addPIF( PLUS, 0);       }
"-"                  { addPIF( MINUS, 0);      }
"/"                  { addPIF( SLASH, 0);      }
"*"                  { addPIF( TIMES, 0);      }
"<"                  { addPIF( LSS, 0);        }
">"                  { addPIF( GTR, 0);        }
"<="                            { addPIF( LEQ, 0);        }
">="                            { addPIF( GEQ, 0);        }
"="                             { addPIF( BECOMES, 0);    }
"=="                            { addPIF( EQ, 0);         }
"{"                             { addPIF( ACOP, 0);       }
"}"                             { addPIF( ACCL, 0);       }
";"                             { addPIF( SEMICOLON, 0);  }
"."                             { addPIF( PERIOD, 0);     }
"("                             { addPIF( LPAREN, 0);     }
")"                             { addPIF( RPAREN, 0);     }
">>"                            { addPIF( INSTR, 0);      }
"<<"                            { addPIF( OUTSTR, 0);     }
"struct"                        { addPIF( STRUCT, 0);     }
"main"                          { addPIF( MAINFNC, 0);    }
"iostream"                      { addPIF( IOSTR, 0);      }
"return"                        { addPIF( RTRNSYM, 0);    }
"#include"                      { addPIF( INCDIR, 0);     }
"using"                         { addPIF( USINGSYM, 0);   }
"namespace"                     { addPIF( NMSSYM, 0);     }
"std"                           { addPIF( STDSYM, 0);     }
"const"                         { addPIF( CONSTSYM, 0);   }
{letter}({letter}|{digit})*                 { addPIF( IDENT, yytext);      }
"0"|((\+)?|(\-)?)[1-9]{digit}               { addPIF( CONSTANT, yytext); }
"\""{letter}"\""                            { addPIF( CONSTANT, yytext);}
([0]|([1-9]{digit}*))"."{digit}*[1-9]       { addPIF( CONSTANT, yytext);}
[ \t\n\r]            /* skip whitespace */
.                    { printf("Unknown character [%c]\n",yytext[0]);}
%%

main( argc, argv )
int argc;
char **argv;
{
    ++argv, --argc; /* skip over program name */
    if ( argc > 0 )
    	yyin = fopen( argv[0], "r" );
    else
     	yyin = stdin;
    yylex();
    print();
}
