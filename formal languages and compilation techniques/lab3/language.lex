%{

#include <string.h>
#include <stdio.h>

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
#define RTRNSYM 31
#define INCDIR 32
#define USINGSYM 33
#define NMSSYM 34
#define STDSYM 35
#define CONSTSYM 36

int pif[5000];
int sym_pos[5000];
char* texts[256];
int ord[256];
int t;

void addPIF(int token, char* identifier) {
    pif[++pif[0]] = token;
    sym_pos[pif[0]] = -1;
    if (identifier != NULL) {
        char *p = (char*)malloc(251);
        p[0] = 0;
        int pos = 0;
        int now = 0;
        while (identifier[now] && ((identifier[now] >= 'a' && identifier[now] <= 'z') || (identifier[now] >= 'A' && identifier[now] <= 'Z') || (identifier[now] >= '0' || identifier[now] <= '9'))) {
            p[pos] = identifier[now];
            ++now;
            ++pos;
        }
        p[pos] = 0;
        if (pos > 250) {
            printf("Too large!");
            exit(2);
        }
        for (int i = 0; i < t; ++i) {
            if (strcmp(texts[i], p) == 0)
            {
                free(p);
                sym_pos[pif[0]] = i;
                return;
            }
        }
        texts[t] = p;
        sym_pos[pif[0]] = t++;
    }
}

void update() {
    for (int i = 0; i < t; ++i)
        ord[i] = i;

    int sorted = 0;
    while (!sorted)
    {
        sorted = 1;
        for (int i = 0; i < t - 1; ++i)
            for (int j = i + 1; j < t; ++j)
                if (strcmp(texts[ord[i]],texts[ord[j]]) > 0) {
                    int aux = ord[i];
                    ord[i] = ord[j];
                    ord[j] = aux;
                    sorted=0;
                }
    }
    int crt = 0;
    for (int i = 1; i <= pif[0]; ++i) {
        if (pif[i] == IDENT || pif[i] == CONSTANT) {
            for (int j = 0; j < t; ++j)
            {
                if (ord[j] == sym_pos[i])
                {
                    sym_pos[i] = j;
                    break;
                }
            }
        }
    }
}

void print() {
    printf("Tokens: %d\n", pif[0]);
    for (int i = 1; i <= pif[0]; ++i) {
        printf("%d->%d, ", pif[i], sym_pos[i]);
    }
    printf("\n\n");
    for (int i = 0; i < t; ++i) {
        printf("%d: %s\n", i, texts[ord[i]]);
    }
}

%}

digit [0-9]
letter [a-zA-Z]

%%
"int"                                       { addPIF( INTSYM, 0);     }
"float"                                     { addPIF( FLOAT, 0);      }
"char"                                      { addPIF( CHARSYM, 0);    }
"cin"                                       { addPIF( INCMD, 0);      }
"cout"                                      { addPIF( OUTCMD, 0);     }
"if"                                        { addPIF( IFSYM, 0);      }
"while"                                     { addPIF( WHILESYM, 0);   }
"else"                                      { addPIF( ELSESYM, 0);    }
"+"                                         { addPIF( PLUS, 0);       }
"-"                                         { addPIF( MINUS, 0);      }
"/"                                         { addPIF( SLASH, 0);      }
"*"                                         { addPIF( TIMES, 0);      }
"<"                                         { addPIF( LSS, 0);        }
">"                                         { addPIF( GTR, 0);        }
"<="                                        { addPIF( LEQ, 0);        }
">="                                        { addPIF( GEQ, 0);        }
"="                                         { addPIF( BECOMES, 0);    }
"=="                                        { addPIF( EQ, 0);         }
"{"                                         { addPIF( ACOP, 0);       }
"}"                                         { addPIF( ACCL, 0);       }
";"                                         { addPIF( SEMICOLON, 0);  }
"."                                         { addPIF( PERIOD, 0);     }
"("                                         { addPIF( LPAREN, 0);     }
")"                                         { addPIF( RPAREN, 0);     }
">>"                                        { addPIF( INSTR, 0);      }
"<<"                                        { addPIF( OUTSTR, 0);     }
"struct"                                    { addPIF( STRUCT, 0);     }
"main"                                      { addPIF( MAINFNC, 0);    }
"iostream.h"                                { addPIF( IOSTR, 0);      }
"return"                                    { addPIF( RTRNSYM, 0);    }
"#include"                                  { addPIF( INCDIR, 0);     }
"using"                                     { addPIF( USINGSYM, 0);   }
"namespace"                                 { addPIF( NMSSYM, 0);     }
"std"                                       { addPIF( STDSYM, 0);     }
"const"                                     { addPIF( CONSTSYM, 0);   }
{letter}({letter}|{digit})*                 { addPIF( IDENT, yytext);}
"0"|((\+)?|(\-)?)[1-9]{digit}*              { addPIF( CONSTANT, yytext);}
"\""{letter}"\""                            { addPIF( CONSTANT, yytext);}
(\+|\-)?([0]|([1-9]{digit}*))"."{digit}*[1-9]       { addPIF( CONSTANT, yytext);}
[ \t\n\r]            /* skip whitespace */
{digit}*{letter}     { printf("Invalid constant, cannot have letter after constant: %10s", yytext); exit(2);}
"0"{digit}           { printf("Cannot have 0 and a digit after it: %10s", yytext); exit(2);}
(\+|\-)[^0-9]          { printf("Constant cannot have something else than a digit after a sign: %10s", yytext); exit(2);}
.                    { printf("Unknown character [%c]\n",yytext[0]); exit(2);}
%%

int main(int argc, char **argv )
{
    ++argv, --argc; /* skip over program name */
    if ( argc > 0 )
    	yyin = fopen( argv[0], "r" );
    else
     	yyin = stdin;
    yylex();
    update();
    print();
    return 0;
}

int yywrap(void){return 1;}
