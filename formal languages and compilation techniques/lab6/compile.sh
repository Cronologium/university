#!/bin/bash

if [ ! -d "./.files" ] ; then
    mkdir .files
fi

bison -d syntax.y -o .files/syntax.tab.c
if [ "$?" -ne 0 ] ; then
    echo "Bison returned errors. Haulting."
else
    echo "Bison OK!"
    echo ""
fi
flex -o .files/lex.yy.c language.lex
if [ "$?" -ne 0 ] ; then
    echo "Flex returned errors. Haulting"
else
    echo "Flex OK!"
    echo ""
fi
g++ .files/lex.yy.c .files/syntax.tab.c -o .files/t++
if [ "$?" -ne 0 ] ; then
    echo "Compiler returned errors. Haulting."
else
    echo "Compiling finished successfully!"
    echo ""
    cd .files
    ./t++ ../$1 
    cd ..
    nasm -f elf64 .files/file.asm -o .files/file.o
    gcc .files/file.o -o $2
    #nasm .files/file.asm -o $2 -f elf64
    #ld -o $2.elf $2 -e main -lc
fi