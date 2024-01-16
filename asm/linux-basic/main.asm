bits 64
global _start
section .text
_start:
    mov rax, 60
    mov rdi, 42
    syscall
    