use crate::lexer::LexicalToken;

pub enum Instruction {
    Pop(String),
    Push(String),
    Mov(String),
    Jmp(String),
    Jz(String),
    Call(String),
    Test(String),
    Cmp(String),
    Cmov(String),
    Addr(String),
    Print,
    Add,
    Sub
}

pub fn parse_tokens(mut tokens: Vec<LexicalToken>) -> Vec<Instruction> {
    let mut instructions = Vec::new();
    let mut jmp_address: usize = 0;
    let mut tokens_parsed: usize = 0;
    let mut address_stack: Vec<usize> = Vec::new();

    while tokens.len() > 0 {
        if let Some(token) = tokens.pop() {
            match token {
                LexicalToken::Keyword(val) => {
                    if val == "pop" {
                        instructions.push(Instruction::Pop(String::from("rbx")));
                    } else if val == "print" {
                        instructions.push(Instruction::Print);
                    } else if val == "dup" {
                        instructions.push(Instruction::Push(String::from("rax")));
                        instructions.push(Instruction::Mov(String::from("rax, [rsp]")));
                    } else if val == "copy" {
                        instructions.push(Instruction::Push(String::from("rax")));
                        instructions.push(Instruction::Mov(String::from("rax, [rsp + 8 * rbx]")));
                        instructions.push(Instruction::Pop(String::from("rbx")));
                    } else if val == "over" {
                        instructions.push(Instruction::Push(String::from("rax")));
                        instructions.push(Instruction::Mov(String::from("rax, [rsp + 8]")));
                    } else if val == "swap" {
                        instructions.push(Instruction::Push(String::from("rbx")));
                        instructions.push(Instruction::Push(String::from("rax")));
                        instructions.push(Instruction::Pop(String::from("rbx")));
                        instructions.push(Instruction::Pop(String::from("rax")));
                    } else if val == "if" {
                        let curr_address = address_stack.pop().expect(
                            &format!("Missing an end, else, or elif keyword. token {}", tokens_parsed + 1)
                        );
                        address_stack.pop().expect(
                            &format!("Missing an end, else, or elif keyword. token {}", tokens_parsed + 1)
                        );

                        instructions.push(Instruction::Jz(curr_address.to_string()));
                        instructions.push(Instruction::Test(String::from("rax, rax")));
                        instructions.push(Instruction::Pop(String::from("rax")));
                    } else if val == "elif" {
                        let curr_address = address_stack.pop().expect("Missing an end keyword");
                        instructions.push(Instruction::Addr(jmp_address.to_string()));
                        instructions.push(Instruction::Jmp(curr_address.to_string()));

                        address_stack.push(curr_address);
                        address_stack.push(jmp_address);
                        jmp_address += 1;
                    } else if val == "else" {
                        let curr_address = address_stack.pop().expect("Missing an end keyword");

                        instructions.push(Instruction::Addr(jmp_address.to_string()));
                        instructions.push(Instruction::Jmp(curr_address.to_string()));

                        address_stack.push(curr_address);
                        address_stack.push(jmp_address);
                        jmp_address += 1;
                    } else if val == "end" {
                        instructions.push(Instruction::Addr(jmp_address.to_string()));
                        address_stack.push(jmp_address);
                        jmp_address += 1;
                    } else if val == "do" {
                        let curr_address = address_stack.pop().expect("Missing an end keyword");

                        instructions.push(Instruction::Jz(curr_address.to_string()));
                        instructions.push(Instruction::Test(String::from("rax, rax")));
                        instructions.push(Instruction::Pop(String::from("rax")));
                    } else if val == "while" {
                        let while_addr = address_stack.pop().expect("Missing an end keyword");
                        instructions.push(Instruction::Addr(while_addr.to_string()));
                    } else if val == "endloop" {
                        let while_addr = jmp_address;

                        address_stack.push(jmp_address);
                        jmp_address += 1;

                        instructions.push(Instruction::Addr(jmp_address.to_string()));
                        address_stack.push(jmp_address);
                        jmp_address += 1;

                        instructions.push(Instruction::Jmp(while_addr.to_string()));
                    }
                }
                LexicalToken::Literal(val) => {
                    instructions.push(Instruction::Push(val));
                }
                LexicalToken::Operator(val) => {
                    if val == "+" {
                        instructions.push(Instruction::Add);

                        instructions.push(Instruction::Pop("rax".parse().unwrap()));
                        instructions.push(Instruction::Pop("rbx".parse().unwrap()));
                    } else if val == "-" {
                        instructions.push(Instruction::Sub);

                        instructions.push(Instruction::Pop("rax".parse().unwrap()));
                        instructions.push(Instruction::Pop("rbx".parse().unwrap()));
                    } else if val == "==" {
                        instructions.push(Instruction::Push(String::from("rcx")));
                        instructions.push(Instruction::Cmov(String::from("e rcx, rdx")));
                        instructions.push(Instruction::Cmp(String::from("rax, rbx")));

                        instructions.push(Instruction::Pop(String::from("rax")));
                        instructions.push(Instruction::Pop(String::from("rbx")));

                        instructions.push(Instruction::Mov(String::from("rdx, 1")));
                        instructions.push(Instruction::Mov(String::from("rcx, 0")));
                    } else if val == ">" {
                        instructions.push(Instruction::Push(String::from("rcx")));
                        instructions.push(Instruction::Cmov(String::from("g rcx, rdx")));
                        instructions.push(Instruction::Cmp(String::from("rax, rbx")));

                        instructions.push(Instruction::Pop(String::from("rax")));
                        instructions.push(Instruction::Pop(String::from("rbx")));

                        instructions.push(Instruction::Mov(String::from("rdx, 1")));
                        instructions.push(Instruction::Mov(String::from("rcx, 0")));
                    } else if val == ">=" {
                        instructions.push(Instruction::Push(String::from("rcx")));
                        instructions.push(Instruction::Cmov(String::from("ge rcx, rdx")));
                        instructions.push(Instruction::Cmp(String::from("rax, rbx")));

                        instructions.push(Instruction::Pop(String::from("rax")));
                        instructions.push(Instruction::Pop(String::from("rbx")));

                        instructions.push(Instruction::Mov(String::from("rdx, 1")));
                        instructions.push(Instruction::Mov(String::from("rcx, 0")));
                    } else if val == "<" {
                        instructions.push(Instruction::Push(String::from("rcx")));
                        instructions.push(Instruction::Cmov(String::from("l rcx, rdx")));
                        instructions.push(Instruction::Cmp(String::from("rax, rbx")));

                        instructions.push(Instruction::Pop(String::from("rax")));
                        instructions.push(Instruction::Pop(String::from("rbx")));

                        instructions.push(Instruction::Mov(String::from("rdx, 1")));
                        instructions.push(Instruction::Mov(String::from("rcx, 0")));
                    } else if val == "<=" {
                        instructions.push(Instruction::Push(String::from("rcx")));
                        instructions.push(Instruction::Cmov(String::from("le rcx, rdx")));
                        instructions.push(Instruction::Cmp(String::from("rax, rbx")));

                        instructions.push(Instruction::Pop(String::from("rax")));
                        instructions.push(Instruction::Pop(String::from("rbx")));

                        instructions.push(Instruction::Mov(String::from("rdx, 1")));
                        instructions.push(Instruction::Mov(String::from("rcx, 0")));
                    }
                }
            }
            tokens_parsed += 1;
        }
    }

    instructions
}
