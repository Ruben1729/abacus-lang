%define SYS_EXIT 60
segment .text
global _start
print:
    mov     r9, -3689348814741910323
    sub     rsp, 40
    mov     BYTE [rsp+31], 10
    lea     rcx, [rsp+30]
.L2:
    mov     rax, rdi
    lea     r8, [rsp+32]
    mul     r9
    mov     rax, rdi
    sub     r8, rcx
    shr     rdx, 3
    lea     rsi, [rdx+rdx*4]
    add     rsi, rsi
    sub     rax, rsi
    add     eax, 48
    mov     BYTE [rcx], al
    mov     rax, rdi
    mov     rdi, rdx
    mov     rdx, rcx
    sub     rcx, 1
    cmp     rax, 9
    ja      .L2
    lea     rax, [rsp+32]
    mov     edi, 1
    sub     rdx, rax
    xor     eax, eax
    lea     rsi, [rsp+32+rdx]
    mov     rdx, r8
    mov     rax, 1
    syscall
    add     rsp, 40
    ret
_start:
   push 0
   push 1
   addr_0:
   mov rax, [rsp + 8]
   push rax
   push 1000
   mov rcx, 0
   mov rdx, 1
   pop rbx
   pop rax
   cmp rax, rbx
   cmovl rcx, rdx
   push rcx
   pop rax
   test rax, rax
   jz addr_1
   mov rax, [rsp + 8]
   push rax
   pop rdi
   call print
   pop rax
   pop rbx
   push rax
   push rbx
   mov rax, [rsp + 8]
   push rax
   pop rbx
   pop rax
   add rbx, rax
   push rbx
   jmp addr_0
   addr_1:
   mov rax, SYS_EXIT
   mov rdi, 0
   syscall
   ret
