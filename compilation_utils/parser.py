from compilation_utils.tokens import LexicalTokens, StackTypes, OperatorTokens, KeywordTokens, \
                                     ConditionalInstructions, StackInstructions, IdentifierInstructions, \
                                     ValueType, LiteralOperations, typesSize
from compilation_utils.asm_generator import asm_generator
from typing import *
from dataclasses import dataclass
import re

iota_counter = -1


def iota(restart=False):
    global iota_counter
    if restart:
        iota_counter = -1
    iota_counter += 1
    return iota_counter


@dataclass
class Var:
    offset: int
    kind: ValueType
    location: (int, int)
    is_const: bool
    len: int


variables: Dict[str, Var] = {}


def generate_asm(instructions):
    condition_stack = []
    functions: Dict[str, int] = {}

    while len(instructions) > 0:
        instruction_type, value, type, deref, location = instructions.pop(0)

        if instruction_type == StackInstructions.PUSH:
            asm_generator.add_assembly_line("    ;; pushing value ;;")
            asm_generator.add_assembly_line("    push %s" % value)
        elif instruction_type == StackInstructions.POP:
            asm_generator.add_assembly_line("    ;; pop value ;;")
            asm_generator.add_assembly_line("    pop eax")
        elif instruction_type == StackInstructions.PRINT:
            asm_generator.add_assembly_line("    ;; print value ;;")
            asm_generator.add_assembly_line("    pop eax")
            if deref:
                asm_generator.add_assembly_line("    mov ebx, [eax]")
                asm_generator.add_assembly_line("    invoke printf, OFFSET num_msg, ebx")
            else:
                asm_generator.add_assembly_line("    invoke printf, OFFSET num_msg, eax")
        elif instruction_type == StackInstructions.PRINT_CHAR:
            asm_generator.add_assembly_line("    ;; print value ;;")
            asm_generator.add_assembly_line("    pop eax")
            if deref:
                asm_generator.add_assembly_line("    mov ebx, [eax]")
                asm_generator.add_assembly_line("    invoke printf, OFFSET char_msg, ebx")
            else:
                asm_generator.add_assembly_line("    invoke printf, OFFSET char_msg, eax")
        elif instruction_type == StackInstructions.FALL:
            asm_generator.add_assembly_line("    ;; fall value ;;")
            asm_generator.add_assembly_line("    pop eax")
            asm_generator.add_assembly_line("    pop ebx")
            if deref:
                asm_generator.add_assembly_line("    mov [esp + 4 * eax], [ebx]")
            else:
                asm_generator.add_assembly_line("    mov [esp + 4 * eax], ebx")
        elif instruction_type == StackInstructions.DUP:
            asm_generator.add_assembly_line("    ;; dup value ;;")
            asm_generator.add_assembly_line("    push [esp]")
            if deref:
                asm_generator.add_assembly_line("    pop eax")
                asm_generator.add_assembly_line("    push [eax]")
        elif instruction_type == StackInstructions.OVER:
            asm_generator.add_assembly_line("    ;; over value ;;")
            asm_generator.add_assembly_line("    push [esp + 4]")
            if deref:
                asm_generator.add_assembly_line("    pop eax")
                asm_generator.add_assembly_line("    push [eax]")
        elif instruction_type == StackInstructions.COPY:
            asm_generator.add_assembly_line("    ;; copy value ;;")
            asm_generator.add_assembly_line("    pop eax")
            asm_generator.add_assembly_line("    push [esp + 4 * eax]")
            if deref:
                asm_generator.add_assembly_line("    pop eax")
                asm_generator.add_assembly_line("    push [eax]")
        elif instruction_type == StackInstructions.SWAP:
            asm_generator.add_assembly_line("    ;; -- swap -- ;;")
            asm_generator.add_assembly_line("    pop eax")
            asm_generator.add_assembly_line("    pop ebx")
            asm_generator.add_assembly_line("    push eax")
            asm_generator.add_assembly_line("    push ebx")
        elif instruction_type == ConditionalInstructions.WHILE or instruction_type == ConditionalInstructions.FOR:
            new_address = (iota(), iota(), KeywordTokens.LOOPS[value])

            condition_stack.append(new_address)

            asm_generator.add_assembly_line("    ;; -- loop -- ;;")
            asm_generator.add_assembly_line("    addr%s:" % new_address[0])
        elif instruction_type == ConditionalInstructions.FN:
            new_address = (iota(), iota(), KeywordTokens.FN_COND)

            condition_stack.append(new_address)

            asm_generator.add_assembly_line("    ;; -- function -- ;;")
            asm_generator.add_assembly_line("    jmp addr%s" % new_address[1])
            asm_generator.add_assembly_line("    addr%s:" % new_address[0])
            asm_generator.add_assembly_line("    mov eax, [esp]")
            asm_generator.add_assembly_line("    mov [ret_stack_end], eax")
            asm_generator.add_assembly_line("    pop eax")

            functions[value] = new_address[0]
        elif instruction_type == ConditionalInstructions.IF:
            condition_stack.append((None, iota(), KeywordTokens.IF_COND))
        elif instruction_type == ConditionalInstructions.ELIF or instruction_type == ConditionalInstructions.ELSE:
            top_addr = condition_stack.pop()

            jmp_addr = top_addr[1]
            end_addr = top_addr[0]

            if top_addr[2] == KeywordTokens.IF_COND:
                end_addr = iota()

            asm_generator.add_assembly_line("    ;; -- %s -- ;;" % token[1])
            asm_generator.add_assembly_line("    jmp addr%d" % end_addr)
            asm_generator.add_assembly_line("    addr%d:" % jmp_addr)

            jmp_addr = iota()

            if KeywordTokens.COND[token[1]] == KeywordTokens.ELSE_COND:
                jmp_addr = end_addr
                end_addr = None

            new_address = (end_addr, jmp_addr, KeywordTokens.COND[token[1]])

            condition_stack.append(new_address)
        elif instruction_type == ConditionalInstructions.END:
            top_addr = condition_stack.pop()

            asm_generator.add_assembly_line("    ;; -- end -- ;;")

            if top_addr[2] == KeywordTokens.FN_COND:
                asm_generator.add_assembly_line("    push [ret_stack_end]")
                asm_generator.add_assembly_line("    ret")

            if top_addr[2] == KeywordTokens.FOR_COND:
                asm_generator.add_assembly_line("    pop eax")
                asm_generator.add_assembly_line("    pop ebx")
                asm_generator.add_assembly_line("    add eax, ebx")
                asm_generator.add_assembly_line("    push ebx")
                asm_generator.add_assembly_line("    push eax")

            if top_addr[2] == KeywordTokens.FOR_COND or top_addr[2] == KeywordTokens.WHILE_COND:
                asm_generator.add_assembly_line("    jmp addr%s" % top_addr[0])

            asm_generator.add_assembly_line("    addr%d:" % top_addr[1])

            if top_addr[2] == KeywordTokens.FOR_COND:
                asm_generator.add_assembly_line("    pop eax")
                asm_generator.add_assembly_line("    pop eax")

        elif instruction_type == ConditionalInstructions.DO:
            top_addr = condition_stack.pop()

            asm_generator.add_assembly_line("    ;; -- do -- ;;")
            asm_generator.add_assembly_line("    pop eax")
            asm_generator.add_assembly_line("    cmp eax, 1")
            asm_generator.add_assembly_line("    jne addr%d" % top_addr[1])

            condition_stack.append(top_addr)
        elif instruction_type == IdentifierInstructions.CREATE:
            asm_generator.add_assembly_line("    ;; let ;;")
            asm_generator.add_assembly_line("    mov eax, OFFSET mem")
            asm_generator.add_assembly_line("    add eax, %s" % variables[value].offset)
            asm_generator.add_assembly_line("    mov ebx, 0")
            asm_generator.add_assembly_line("    mov [eax], ebx")
        elif instruction_type == IdentifierInstructions.UPDATE:
            asm_generator.add_assembly_line("    ;; pushing identifier ;;")
            asm_generator.add_assembly_line("    mov eax, OFFSET mem")
            asm_generator.add_assembly_line("    add eax, %s" % variables[value].offset)
            asm_generator.add_assembly_line("    push eax")
        elif instruction_type == IdentifierInstructions.FUNCTION:
            asm_generator.add_assembly_line("    ;; calling function ;;")
            asm_generator.add_assembly_line("    call addr%d" % functions[value])
        elif instruction_type == IdentifierInstructions.SIZEOF:
            asm_generator.add_assembly_line("    push %s" % variables[value].len)
        elif value in LiteralOperations:
            asm_generator.add_assembly_line("    ;; performing %s ;;" % value)
            asm_generator.add_assembly_line("    pop eax")
            asm_generator.add_assembly_line("    pop ebx")

            if value in OperatorTokens.BASIC:
                asm_generator.add_assembly_line("    %s ebx, eax" % OperatorTokens.BASIC[value])
                asm_generator.add_assembly_line("    push ebx")
            elif value in OperatorTokens.DIV:
                asm_generator.add_assembly_line("    xor edx, edx")
                asm_generator.add_assembly_line("    div ebx")
                asm_generator.add_assembly_line("    push %s" % OperatorTokens.DIV[value])
            elif value in OperatorTokens.CONDITIONS:
                asm_generator.add_assembly_line("    xor ecx, ecx")
                asm_generator.add_assembly_line("    mov edx, 1")
                asm_generator.add_assembly_line("    cmp ebx, eax")
                asm_generator.add_assembly_line("    cmov%s ecx, edx" % OperatorTokens.CONDITIONS[value])
                asm_generator.add_assembly_line("    push ecx")
            elif value == "=":
                asm_generator.add_assembly_line("    mov [eax], ebx")


def parse_tokens(tokens):
    is_comment = False
    condition_stack = []
    instructions = []

    # instruction_type, value, type, deref, location
    while len(tokens) > 0:
        token = tokens.pop(0)

        # Ignores tokens when there's a comment
        if is_comment:
            if token[0] == LexicalTokens.NEWLINE:
                is_comment = False
            continue

        # Keywords: print, pop, swap
        if token[0] == LexicalTokens.KEYWORD:
            if token[1] == "dup" or token[1] == "[dup]":
                instructions.append((StackInstructions.DUP, None, None, token[1] == "[dup]", token[2]))
            elif token[1] == "copy" or token[1] == "[copy]":
                instructions.append((StackInstructions.COPY, None, None, token[1] == "[copy]", token[2]))
            elif token[1] == "over" or token[1] == "[over]":
                instructions.append((StackInstructions.OVER, None, None, token[1] == "[over]", token[2]))
            elif token[1] == "print" or token[1] == "[print]":
                instructions.append((StackInstructions.PRINT, None, None, token[1] == "[print]", token[2]))
            elif token[1] == "print_char" or token[1] == "[print_char]":
                instructions.append((StackInstructions.PRINT_CHAR, None, None, token[1] == "[print_char]", token[2]))
            elif token[1] == "fall" or token[1] == "[fall]":
                instructions.append((StackInstructions.FALL, None, None, token[1] == "[fall]", token[2]))
            elif token[1] == "pop":
                instructions.append((StackInstructions.POP, None, None, False, token[2]))
            elif token[1] == "sizeof":
                curr_token = None
                while len(tokens) > 0:
                    curr_token = tokens.pop(0)
                    if curr_token[0] != LexicalTokens.WHITE_SPACE and curr_token[0] != LexicalTokens.NEWLINE:
                        break

                assert curr_token[0] == LexicalTokens.IDENTIFIER, "%s:%s -> Error: Expected identifier got %s." %\
                                                                  (curr_token[2][0], curr_token[2][1], curr_token[0])

                instructions.append((IdentifierInstructions.SIZEOF, curr_token[1], None, False, token[2]))

            elif token[1] == "swap":
                instructions.append((StackInstructions.SWAP, None, None, False, token[2]))
            elif token[1] == "if":
                instructions.append((ConditionalInstructions.IF, None, None, False, token[2]))
            elif token[1] == "while":
                instructions.append((ConditionalInstructions.WHILE, 'while', None, False, token[2]))
            elif token[1] == "for":
                instructions.append((ConditionalInstructions.FOR, 'for', None, False, token[2]))
            elif token[1] == "fn":
                instructions.append((ConditionalInstructions.FN, 'fn', None, False, token[2]))
            elif token[1] == "elif":
                instructions.append((ConditionalInstructions.ELIF, None, None, False, token[2]))
            elif token[1] == "else":
                instructions.append((ConditionalInstructions.ELSE, None, None, False, token[2]))
            elif token[1] == "do":
                instructions.append((ConditionalInstructions.DO, None, None, False, token[2]))
            elif token[1] == "end":
                instructions.append((ConditionalInstructions.END, None, None, False, token[2]))
            elif token[1] == "let" or token[1] == "const":
                curr_token = None
                while len(tokens) > 0:
                    curr_token = tokens.pop(0)
                    if curr_token[0] != LexicalTokens.WHITE_SPACE and curr_token[0] != LexicalTokens.NEWLINE:
                        break

                assert StackTypes.getId(curr_token[1]) in typesSize, "%s:%s -> Error: Expected type got %s." %\
                                                                  (curr_token[2][0], curr_token[2][1], curr_token[0])

                var_size = typesSize[StackTypes.getId(curr_token[1])]
                kind = StackTypes.getId(curr_token[1])

                while len(tokens) > 0:
                    curr_token = tokens.pop(0)
                    if curr_token[0] != LexicalTokens.WHITE_SPACE and curr_token[0] != LexicalTokens.NEWLINE:
                        break

                if curr_token[0] == LexicalTokens.MODIFIER:
                    match = re.search(r'\d+', curr_token[1])
                    var_size *= int(match.group(0))

                    kind = StackTypes.PTR

                    while len(tokens) > 0:
                        curr_token = tokens.pop(0)
                        if curr_token[0] != LexicalTokens.WHITE_SPACE and curr_token[0] != LexicalTokens.NEWLINE:
                            break

                assert curr_token[0] == LexicalTokens.IDENTIFIER, "%s:%s -> Error: Expected identifier got %s." % \
                                                                  (curr_token[2][0], curr_token[2][1], curr_token[0])

                var_offset = 0
                for i, var in variables.items():
                    var_offset += var.len

                variables[curr_token[1]] = (Var(offset=var_offset, kind=kind, location=curr_token[2], is_const=(token[1] == "const"), len=var_size))

                instructions.append((IdentifierInstructions.CREATE, curr_token[1], None, False, token[2]))

        # Identifiers: user defined variables
        elif token[0] == LexicalTokens.IDENTIFIER:
            if token[1] in variables:
                instructions.append((IdentifierInstructions.UPDATE, token[1], None, False, token[2]))

        # Literals: any numeric value
        elif token[0] == LexicalTokens.LITERAL:
            instructions.append((StackInstructions.PUSH, token[1], StackTypes.INT, False, token[2]))

        # String Literals: "Hello World!"
        elif token[0] == LexicalTokens.STRING_LITERAL:
            pass

        elif token[0] == LexicalTokens.COMMENT:
            is_comment = True

        # Operators: +, -, /, %
        elif token[0] == LexicalTokens.OPERATOR:
            instructions.append((token[0], token[1], None, False, token[2]))

        elif token[0] == LexicalTokens.WHITE_SPACE or token[0] == LexicalTokens.NEWLINE:
            continue

        else:
            assert False, "%s:%s -> Error: word %s for token %s not implemented" % (
                token[2][0], token[2][1], token[1], token[0])

    return instructions


def static_type_check(instructions):
    condition_stack = []
    functions: Dict[str, int] = {}
    stack = []

    while len(instructions) > 0:
        instruction_type, value, type, deref, location = instructions.pop(0)

        if instruction_type == StackInstructions.PUSH:
            stack.append((value, type))
        elif instruction_type == StackInstructions.POP:
            assert len(stack) >= 1, "%s:%s -> Error: Unable to pop empty stack." % location
            stack.pop()
        elif instruction_type == StackInstructions.PRINT:
            assert len(stack) >= 1, "%s:%s -> Error: Unable to print empty stack." % location
            stack.pop()
        elif instruction_type == StackInstructions.FALL:
            # TODO
            pass
        elif instruction_type == StackInstructions.DUP:
            assert len(stack) >= 1, "%s:%s -> Error: Unable to duplicate empty stack." % location
            stack.append(stack[len(stack) - 1])
        elif instruction_type == StackInstructions.OVER:
            assert len(stack) >= 2, "%s:%s -> Error: Unable to copy item, not enough items in the stack." % location
            stack.append(stack[len(stack) - 2])
        elif instruction_type == StackInstructions.COPY:
            curr_val, curr_type = stack.pop()
            assert curr_type == StackTypes.INT, "%s:%s -> Error: Unexpected parameter, copy requires an integer." % location
            assert len(stack) >= (curr_val + 1), "%s:%s -> Error: Unable to copy item, not enough items in the stack." % location
            stack.append(stack[len(stack) - (curr_val + 1)])
        elif instruction_type == StackInstructions.SWAP:
            top_stack = stack.pop()

            asm_generator.add_assembly_line("    ;; -- swap -- ;;")
            asm_generator.add_assembly_line("    pop eax")
            asm_generator.add_assembly_line("    pop ebx")
            asm_generator.add_assembly_line("    push eax")
            asm_generator.add_assembly_line("    push ebx")
        elif instruction_type == ConditionalInstructions.WHILE or instruction_type == ConditionalInstructions.FOR:
            new_address = (iota(), iota(), KeywordTokens.LOOPS[value])

            condition_stack.append(new_address)

            asm_generator.add_assembly_line("    ;; -- loop -- ;;")
            asm_generator.add_assembly_line("    addr%s:" % new_address[0])
            pass
        elif instruction_type == ConditionalInstructions.FN:
            new_address = (iota(), iota(), KeywordTokens.FN_COND)

            condition_stack.append(new_address)

            asm_generator.add_assembly_line("    ;; -- function -- ;;")
            asm_generator.add_assembly_line("    jmp addr%s" % new_address[1])
            asm_generator.add_assembly_line("    addr%s:" % new_address[0])
            asm_generator.add_assembly_line("    mov eax, [esp]")
            asm_generator.add_assembly_line("    mov [ret_stack_end], eax")
            asm_generator.add_assembly_line("    pop eax")

            functions[value] = new_address[0]
        elif instruction_type == ConditionalInstructions.IF:
            condition_stack.append((None, iota(), KeywordTokens.IF_COND))
        elif instruction_type == ConditionalInstructions.ELIF or instruction_type == ConditionalInstructions.ELSE:
            top_addr = condition_stack.pop()

            jmp_addr = top_addr[1]
            end_addr = top_addr[0]

            if top_addr[2] == KeywordTokens.IF_COND:
                end_addr = iota()

            asm_generator.add_assembly_line("    ;; -- %s -- ;;" % token[1])
            asm_generator.add_assembly_line("    jmp addr%d" % end_addr)
            asm_generator.add_assembly_line("    addr%d:" % jmp_addr)

            jmp_addr = iota()

            if KeywordTokens.COND[token[1]] == KeywordTokens.ELSE_COND:
                jmp_addr = end_addr
                end_addr = None

            new_address = (end_addr, jmp_addr, KeywordTokens.COND[token[1]])

            condition_stack.append(new_address)
        elif instruction_type == ConditionalInstructions.END:
            top_addr = condition_stack.pop()

            asm_generator.add_assembly_line("    ;; -- end -- ;;")

            if top_addr[2] == KeywordTokens.FN_COND:
                asm_generator.add_assembly_line("    push [ret_stack_end]")
                asm_generator.add_assembly_line("    ret")

            if top_addr[2] == KeywordTokens.FOR_COND:
                asm_generator.add_assembly_line("    pop eax")
                asm_generator.add_assembly_line("    pop ebx")
                asm_generator.add_assembly_line("    add eax, ebx")
                asm_generator.add_assembly_line("    push ebx")
                asm_generator.add_assembly_line("    push eax")

            if top_addr[2] == KeywordTokens.FOR_COND or top_addr[2] == KeywordTokens.WHILE_COND:
                asm_generator.add_assembly_line("    jmp addr%s" % top_addr[0])

            asm_generator.add_assembly_line("    addr%d:" % top_addr[1])

            if top_addr[2] == KeywordTokens.FOR_COND:
                asm_generator.add_assembly_line("    pop eax")
                asm_generator.add_assembly_line("    pop eax")

        elif instruction_type == ConditionalInstructions.DO:
            top_addr = condition_stack.pop()

            asm_generator.add_assembly_line("    ;; -- do -- ;;")
            asm_generator.add_assembly_line("    pop eax")
            asm_generator.add_assembly_line("    cmp eax, 1")
            asm_generator.add_assembly_line("    jne addr%d" % top_addr[1])

            condition_stack.append(top_addr)
        elif instruction_type == IdentifierInstructions.CREATE:
            asm_generator.add_assembly_line("    ;; let ;;")
            asm_generator.add_assembly_line("    mov eax, OFFSET mem")
            asm_generator.add_assembly_line("    add eax, %s" % variables[value].offset)
            asm_generator.add_assembly_line("    mov ebx, 0")
            asm_generator.add_assembly_line("    mov [eax], ebx")
        elif instruction_type == IdentifierInstructions.UPDATE:
            asm_generator.add_assembly_line("    ;; pushing identifier ;;")
            asm_generator.add_assembly_line("    mov eax, OFFSET mem")
            asm_generator.add_assembly_line("    add eax, %s" % variables[value].offset)
            asm_generator.add_assembly_line("    push eax")
        elif instruction_type == IdentifierInstructions.FUNCTION:
            asm_generator.add_assembly_line("    ;; calling function ;;")
            asm_generator.add_assembly_line("    call addr%d" % functions[value])
        elif instruction_type == IdentifierInstructions.SIZEOF:
            asm_generator.add_assembly_line("    push %s" % variables[value].len)
        elif value in LiteralOperations:
            assert len(stack) >= 2, "%s:%s -> Error: Operations require at least two integers at the top of the stack." % location

            curr_val, curr_type = stack.pop()

            assert (curr_type == StackTypes.INT and stack[len(stack) - 1][1] == StackTypes.INT), \
                "%s:%s -> Error: Operations require the top two items in the stack to be integers." % location

            if value == "=":
                stack.pop()

