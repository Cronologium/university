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
FILE* asm_file;

#define save_all(out) \
    fprintf(out, "push rdi\n"); \
    fprintf(out, "push rsi\n"); \
    fprintf(out, "push rbp\n");

#define get_all(out) \
    fprintf(out, "pop rbp\n"); \
    fprintf(out, "pop rsi\n"); \
    fprintf(out, "pop rdi\n"); \


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

int do_eval(FILE* out, int i) {
    int initially = i;
    if (pif[i] == CONSTANT) {
        fprintf(out, "mov rax, %s\n", texts[sym_pos[i]]);
    } else {
        fprintf(out, "mov rax, [%s]\n", texts[sym_pos[i]]);
    }
    while (pif[i+1] > ELSESYM && pif[i+1] < LSS) {
        switch(pif[i+1]) {
            case PLUS:
                fprintf(out, "adc");
                break;
            case MINUS:
                fprintf(out, "sbb");
                break;
            case TIMES:
                fprintf(out, "imul");
                break;
            case SLASH:
                fprintf(out, "idiv");
                break;
        }
        if (pif[i+2] == CONSTANT) {
            fprintf(out, " rax, %s\n", texts[sym_pos[i+2]]);
        } else {
            fprintf(out, " rax, [%s]\n", texts[sym_pos[i+2]]);
        }
        i += 2;
    }
    return i - initially + 1;
}

int do_assign(FILE* out, int i) {
    if (pif[i+2] == CONSTANT) {
        fprintf(out, "mov qword [%s], %s\n", texts[sym_pos[i]], texts[sym_pos[i+2]]);   
        return 3;                
    } else {
        int size = do_eval(out, i+2);
        fprintf(out, "mov [%s], rax\n", texts[sym_pos[i]]);
        return 2 + size;
    }
}

int do_statement_list(FILE* out, int i) {
    int initially = i;
    i += 1;
    while (pif[i] != ACCL) {
        int size = 0;
        if (pif[i] == SEMICOLON) {
            i += 1;
            continue;
        }
        switch(pif[i]) {
            case INTSYM:
                if (pif[i+2] == BECOMES) {
                    size = do_assign(out, i+1);
                    i += size + 1;
                } else {
                    i += 2;
                }
                break;
            case IDENT:
                size = do_assign(out, i);
                i += size;
                break;
            case IFSYM:
                do_eval(out, i+2);
                fprintf(out, "cmp rax, 0\nje else%d:\n", i);
                size = do_statement_list(out, i+4);
                fprintf(out, "else%d:", i);
                i += size + 4;
                break;
            case PRINTF:
                save_all(out);
                fprintf(out, "mov rsi, [%s]\n", texts[sym_pos[i+4]]);
                fprintf(out, "mov rdi, msg_\n");
                fprintf(out, "call printf\n");
                get_all(out);
                i += 6;
                break;
            case SCANF:
                save_all(out);
                fprintf(out, "mov rsi, %s\n", texts[sym_pos[i+5]]);
                fprintf(out, "mov rdi, msg_\n");
                fprintf(out, "call scanf\n");
                get_all(out);
                fprintf(out, "mov rax, qword [%s]\n", texts[sym_pos[i+5]]);
                i += 7;
                break;
            case RTRNSYM:
                fprintf(out, "push 0\n");
                fprintf(out, "call exit\n\n");
                
                i += 2;
                break;
        }           
    }
    return i - initially + 1;
}

void update(FILE* out) {
    fprintf(out, "global main\n\n");
    fprintf(out, "extern printf\n");
    fprintf(out, "extern scanf\n");
    fprintf(out, "extern exit\n\n");
    fprintf(out, "SECTION .text\n\n");
    fprintf(out, "main:\n");

    do_statement_list(out, 9);

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
    fprintf(out, "\nsection .data\n");
    for (int i = 0; i < t; ++i) {
        if (texts[i][0] < '0' || texts[i][0] > '9') {
            fprintf(out, "\t%s:\t\tdq 0\n", texts[i]);
        }
    }
    fprintf(out, "\tmsg_:\t\tdb \"%%d\", 0\n");
}

void print() {
    printf("Tokens: %d\n", pif[0]);
    for (int i = 1; i <= pif[0]; ++i) {
        printf("%d <==> %d->%d\n", i, pif[i], sym_pos[i]);
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
"if"                                        { addPIF( IFSYM, 0);      return IFSYM;}
"while"                                     { addPIF( WHILESYM, 0);   return WHILESYM;}
"else"                                      { addPIF( ELSESYM, 0);    return ELSESYM;}
"+"                                         { addPIF( PLUS, 0);       return PLUS;}
"-"                                         { addPIF( MINUS, 0);      return MINUS;}
"/"                                         { addPIF( SLASH, 0);      return SLASH;}
"*"                                         { addPIF( TIMES, 0);      return TIMES;}
"<"                                         { addPIF( LSS, 0);        return LSS;}
">"                                         { addPIF( GTR, 0);        return GTR;}
"="                                         { addPIF( BECOMES, 0);    return BECOMES;}
"{"                                         { addPIF( ACOP, 0);       return ACOP;}
"}"                                         { addPIF( ACCL, 0);       return ACCL;}
";"                                         { addPIF( SEMICOLON, 0);  return SEMICOLON;}
","                                         { addPIF( COMMA, 0);      return COMMA;}
"("                                         { addPIF( LPAREN, 0);     return LPAREN;}
")"                                         { addPIF( RPAREN, 0);     return RPAREN;}
"&"                                         { addPIF( AMP, 0);        return AMP;}
"main"                                      { addPIF( MAINFNC, 0);    return MAINFNC;}
"cstdio"                                    { addPIF( STDIO, 0);      return STDIO;}
"return"                                    { addPIF( RTRNSYM, 0);    return RTRNSYM;}
"#include"                                  { addPIF( INCDIR, 0);     return INCDIR;}
"const"                                     { addPIF( CONSTSYM, 0);   return CONSTSYM;}
"scanf"                                     { addPIF( SCANF, 0);      return SCANF;}
"printf"                                    { addPIF( PRINTF, 0);     return PRINTF;}
"\"%d\""                                    { addPIF( INTFMT, 0);     return INTFMT;}

{letter}({letter}|{digit})*                 { addPIF( IDENT, yytext); return IDENT;}
"0"|((\+)?|(\-)?)[1-9]{digit}*              { addPIF( CONSTANT, yytext); return CONSTANT;}
[ \t\r]            /* skip whitespace */
{digit}*{letter}     { printf("Invalid constant, cannot have letter after constant: %10s", yytext); exit(2);}
"0"{digit}           { printf("Cannot have 0 and a digit after it: %10s", yytext); exit(2);}
.                    { printf("Unknown character [%c]\n",yytext[0]); exit(2);}
[\n]                lineNo++;
%%
