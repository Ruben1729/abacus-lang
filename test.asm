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
    num_msg db "%d", 13, 10, 0
    char_msg db "%c", 0

.data?
    ret_stack dword 8192 dup(?)
    ret_stack_end dword 1 dup(?)
    mem dword 8192 dup(?)


.code

main:
    ;; -- function -- ;;
    jmp addr1
    addr0:
    mov eax, [esp]
    mov [ret_stack_end], eax
    pop eax
    ;; print value ;;
    pop eax
    invoke printf, OFFSET num_msg, eax
    ;; -- loop -- ;;
    addr2:
    ;; dup value ;;
    push [esp]
    ;; pushing value ;;
    push 0
    ;; performing != ;;
    pop eax
    pop ebx
    xor ecx, ecx
    mov edx, 1
    cmp ebx, eax
    cmovne ecx, edx
    push ecx
    ;; -- do -- ;;
    pop eax
    cmp eax, 1
    jne addr3
    ;; print value ;;
    pop eax
    invoke printf, OFFSET char_msg, eax
    ;; -- end -- ;;
    jmp addr2
    addr3:
    ;; -- end -- ;;
    push [ret_stack_end]
    ret
    addr1:
    ;; pushing value ;;
    push 0
    ;; pushing value ;;
    push 100
    ;; pushing value ;;
    push 108
    ;; pushing value ;;
    push 114
    ;; pushing value ;;
    push 111
    ;; pushing value ;;
    push 119
    ;; pushing value ;;
    push 32
    ;; pushing value ;;
    push 111
    ;; pushing value ;;
    push 108
    ;; pushing value ;;
    push 108
    ;; pushing value ;;
    push 101
    ;; pushing value ;;
    push 72
    ;; print value ;;
    pop eax
    invoke printf, OFFSET num_msg, eax
    exit_addr:
    invoke ExitProcess, 0
end main
