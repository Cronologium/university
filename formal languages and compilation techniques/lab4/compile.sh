#!/bin/bash

bison -d syntax.y
if [ "$?" -ne 0 ] ; then
    echo "Bison returned errors. Haulting."
else
    echo "Bison OK!"
    echo ""
fi
flex language.lex
if [ "$?" -ne 0 ] ; then
    echo "Flex returned errors. Haulting"
else
    echo "Flex OK!"
    echo ""
fi
g++ lex.yy.c syntax.tab.c
if [ "$?" -ne 0 ] ; then
    echo "Compiler returned errors. Haulting."
else
    echo "Compiling finished successfully!"
    echo ""
    ./a.out $1
fi