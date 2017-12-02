%{

#include <string.h>
#include <stdio.h>
#include "syntax.tab.h"

int pif[5000];
int sym_pos[5000];
char* texts[256];
int lineNo = 1;
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

%option noyywrap
digit [0-9]
letter [a-zA-Z]

%%
"int"                                       { addPIF( INTSYM, 0);     return INTSYM;}
"float"                                     { addPIF( FLOAT, 0);      return FLOAT;}
"char"                                      { addPIF( CHARSYM, 0);    return CHARSYM;}
"cin"                                       { addPIF( INCMD, 0);      return INCMD;}
"cout"                                      { addPIF( OUTCMD, 0);     return OUTCMD;}
"if"                                        { addPIF( IFSYM, 0);      return IFSYM;}
"while"                                     { addPIF( WHILESYM, 0);   return WHILESYM;}
"else"                                      { addPIF( ELSESYM, 0);    return ELSESYM;}
"+"                                         { addPIF( PLUS, 0);       return PLUS;}
"-"                                         { addPIF( MINUS, 0);      return MINUS;}
"/"                                         { addPIF( SLASH, 0);      return SLASH;}
"*"                                         { addPIF( TIMES, 0);      return TIMES;}
"<"                                         { addPIF( LSS, 0);        return LSS;}
">"                                         { addPIF( GTR, 0);        return GTR;}
"<="                                        { addPIF( LEQ, 0);        return LEQ;}
">="                                        { addPIF( GEQ, 0);        return GEQ;}
"="                                         { addPIF( BECOMES, 0);    return BECOMES;}
"=="                                        { addPIF( EQ, 0);         return EQ;}
"!="                                        { addPIF( NEQ, 0);        return NEQ;}
"{"                                         { addPIF( ACOP, 0);       return ACOP;}
"}"                                         { addPIF( ACCL, 0);       return ACCL;}
";"                                         { addPIF( SEMICOLON, 0);  return SEMICOLON;}
"."                                         { addPIF( PERIOD, 0);     return PERIOD;}
"("                                         { addPIF( LPAREN, 0);     return LPAREN;}
")"                                         { addPIF( RPAREN, 0);     return RPAREN;}
">>"                                        { addPIF( INSTR, 0);      return INSTR;}
"<<"                                        { addPIF( OUTSTR, 0);     return OUTSTR;}
"struct"                                    { addPIF( STRUCT, 0);     return STRUCT;}
"main"                                      { addPIF( MAINFNC, 0);    return MAINFNC;}
"iostream.h"                                { addPIF( IOSTR, 0);      return IOSTR;}
"return"                                    { addPIF( RTRNSYM, 0);    return RTRNSYM;}
"#include"                                  { addPIF( INCDIR, 0);     return INCDIR;}
"using"                                     { addPIF( USINGSYM, 0);   return USINGSYM;}
"namespace"                                 { addPIF( NMSSYM, 0);     return NMSSYM;}
"std"                                       { addPIF( STDSYM, 0);     return STDSYM;}
"const"                                     { addPIF( CONSTSYM, 0);   return CONSTSYM;}
{letter}({letter}|{digit})*                 { addPIF( IDENT, yytext); return IDENT;}
"0"|((\+)?|(\-)?)[1-9]{digit}*              { addPIF( CONSTANT, yytext); return CONSTANT;}
"\""{letter}"\""                            { addPIF( CONSTANT, yytext); return CONSTANT;}
(\+|\-)?([0]|([1-9]{digit}*))"."{digit}*[1-9]       { addPIF( CONSTANT, yytext); return CONSTANT;}
[ \t\r]            /* skip whitespace */
{digit}*{letter}     { printf("Invalid constant, cannot have letter after constant: %10s", yytext); exit(2);}
"0"{digit}           { printf("Cannot have 0 and a digit after it: %10s", yytext); exit(2);}
.                    { printf("Unknown character [%c]\n",yytext[0]); exit(2);}
[\n]                lineNo++;
%%
