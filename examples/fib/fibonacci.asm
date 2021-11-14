.686
.model flat, stdcall
option casemap : none
include    \masm32\include\kernel32.inc
include    \masm32\include\masm32.inc
include    \masm32\include\msvcrt.inc
includelib \masm32\lib\kernel32.lib
includelib \masm32\lib\masm32.lib
includelib \masm32\lib\msvcrt.lib

printf PROTO C, :VARARG

.data
    message db "%d", 13, 10, 0

.data?
    ret_stack dword 8192 dup(?)
    ret_stack_end dword 1 dup(?)
    mem dword 8192 dup(?)


.code

main:
    ;; pushing literal ;;
    push 0
    ;; pushing literal ;;
    push 1
    ;; -- loop -- ;;
    addr0:
    ;; -- duplicate -- ;;
    push [esp + 4]
    ;; pushing literal ;;
    push 1000
    ;; performing < ;;
    pop eax
    pop ebx
    xor ecx, ecx
    mov edx, 1
    cmp ebx, eax
    cmovl ecx, edx
    push ecx
    ;; -- do -- ;;
    pop eax
    cmp eax, 1
    jne addr1
    ;; -- duplicate -- ;;
    push [esp + 4]
    pop eax
    invoke printf, OFFSET message, eax
    ;; -- swap -- ;;
    pop eax
    pop ebx
    push eax
    push ebx
    ;; -- duplicate -- ;;
    push [esp + 4]
    ;; performing + ;;
    pop eax
    pop ebx
    add ebx, eax
    push ebx
    ;; -- end -- ;;
    jmp addr0
    addr1:
    exit_addr:
    invoke ExitProcess, 0
end main
