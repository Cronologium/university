global main

extern printf
extern scanf
extern exit

SECTION .text

main:
push rdi
push rsi
push rbp
mov rsi, a
mov rdi, msg_
call scanf
pop rbp
pop rsi
pop rdi
mov rax, qword [a]
push rdi
push rsi
push rbp
mov rsi, b
mov rdi, msg_
call scanf
pop rbp
pop rsi
pop rdi
mov rax, qword [b]
mov rax, [a]
imul rax, [b]
mov [sum], rax
push rdi
push rsi
push rbp
mov rsi, [sum]
mov rdi, msg_
call printf
pop rbp
pop rsi
pop rdi
push 0
call exit


section .data
	a:		dq 0
	b:		dq 0
	sum:		dq 0
	msg_:		db "%d", 0
