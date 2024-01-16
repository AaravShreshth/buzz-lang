bits 64 

section .text
global write

write:
    mov rax, 1
    mov rdi, 1
    mov rsi, rdx 
    mov rdx, rcx
    syscall
    ret

section .data  
libname db "STDIO", 0ah 
liblen equ $-libname