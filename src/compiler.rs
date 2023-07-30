use std::fs::File;
use std::io;
use std::io::Write;
use std::path::Path;
use crate::parser::Instruction;
use std::process::Command;

pub struct Compiler {
    project: String,
    writer: io::BufWriter<File>
}

impl Compiler {
    pub fn new(mut project_name: &str) -> Self {
        let extension = ".aba";

        project_name = if project_name.ends_with(extension) {
            let without_extension = &project_name[0..project_name.len()-extension.len()];
            without_extension
        } else {
            panic!("Cannot recognize the extension.");
        };

        let path_name = format!("{}.asm", project_name);

        let path = Path::new(&path_name);
        let file = File::create(&path).expect("Unable to create assembly.");

        Compiler {
            project: String::from(project_name),
            writer: io::BufWriter::new(file)
        }
    }

    pub fn init(&mut self) {
        self.write_line("%define SYS_EXIT 60");
        self.write_line("segment .text");
        self.write_line("global _start");

        self.write_line("print:"                               );
        self.write_line("    mov     r9, -3689348814741910323" );
        self.write_line("    sub     rsp, 40"                  );
        self.write_line("    mov     BYTE [rsp+31], 10"        );
        self.write_line("    lea     rcx, [rsp+30]"            );
        self.write_line(".L2:"                                 );
        self.write_line("    mov     rax, rdi"                 );
        self.write_line("    lea     r8, [rsp+32]"             );
        self.write_line("    mul     r9"                       );
        self.write_line("    mov     rax, rdi"                 );
        self.write_line("    sub     r8, rcx"                  );
        self.write_line("    shr     rdx, 3"                   );
        self.write_line("    lea     rsi, [rdx+rdx*4]"         );
        self.write_line("    add     rsi, rsi"                 );
        self.write_line("    sub     rax, rsi"                 );
        self.write_line("    add     eax, 48"                  );
        self.write_line("    mov     BYTE [rcx], al"           );
        self.write_line("    mov     rax, rdi"                 );
        self.write_line("    mov     rdi, rdx"                 );
        self.write_line("    mov     rdx, rcx"                 );
        self.write_line("    sub     rcx, 1"                   );
        self.write_line("    cmp     rax, 9"                   );
        self.write_line("    ja      .L2"                      );
        self.write_line("    lea     rax, [rsp+32]"            );
        self.write_line("    mov     edi, 1"                   );
        self.write_line("    sub     rdx, rax"                 );
        self.write_line("    xor     eax, eax"                 );
        self.write_line("    lea     rsi, [rsp+32+rdx]"        );
        self.write_line("    mov     rdx, r8"                  );
        self.write_line("    mov     rax, 1"                   );
        self.write_line("    syscall"                          );
        self.write_line("    add     rsp, 40"                  );
        self.write_line("    ret"                              );

        self.write_line("_start:");
    }

    pub fn write_line(&mut self, val: &str) {
        self.writer.write(val.as_ref()).expect("Unable to insert value.");
        self.writer.write(b"\n").expect("Unable to insert new line.");
    }

    pub fn generate_assembly(&mut self, mut instructions: Vec<Instruction>) {
        while instructions.len() > 0 {
            if let Some(instruction) = instructions.pop() {
                match instruction {
                    Instruction::Pop(val) => {
                        self.write_line(format!("   pop {}", val).as_ref());
                    }
                    Instruction::Push(val) => {
                        self.write_line(format!("   push {}", val).as_ref());
                    }
                    Instruction::Mov(val) => {
                        self.write_line(format!("   mov {}", val).as_ref())
                    },
                    Instruction::Print => {
                        self.write_line("   pop rdi");
                        self.write_line("   call print");
                    }
                    Instruction::Add => {
                        self.write_line("   add rbx, rax");
                        self.write_line("   push rbx");
                    }
                    Instruction::Sub => {
                        self.write_line("   sub rbx, rax");
                        self.write_line("   push rbx");
                    }
                    Instruction::Jmp(val) => {
                        self.write_line(format!("   jmp addr_{}", val).as_ref());
                    }
                    Instruction::Jz(val) => {
                        self.write_line(format!("   jz addr_{}", val).as_ref());
                    }
                    Instruction::Test(val) => {
                        self.write_line(format!("   test {}", val).as_ref());
                    }
                    Instruction::Cmp(val) => {
                        self.write_line(format!("   cmp {}", val).as_ref());
                    }
                    Instruction::Cmov(val) => {
                        self.write_line(format!("   cmov{}", val).as_ref());
                    }
                    Instruction::Call(val) => {
                        self.write_line(format!("   call {}", val).as_ref());
                    }
                    Instruction::Addr(val) => {
                        self.write_line(format!("   addr_{}:", val).as_ref());
                    }
                }
            }
        }

        self.write_line("   mov rax, SYS_EXIT");
        self.write_line("   mov rdi, 0");
        self.write_line("   syscall");
        self.write_line("   ret");
    }

    pub fn compile(&mut self) {
        let path = Path::new(&self.project);
        let directory = path.parent().unwrap();  // Parent directory of the file
        let file_stem = path.file_stem().unwrap();

        // Run "nasm -felf64 test.asm"
        let mut output_nasm = Command::new("nasm");
        output_nasm.args(&["-felf64", &format!("{}.asm", &file_stem.to_str().unwrap())]);

        println!("Compiling... {:?}", output_nasm);

        let nasm_result = output_nasm.output().expect("Failed to compile");

        // Print output of nasm command
        if !nasm_result.status.success() {
            eprintln!("Command executed with error:");
            eprintln!("stdout: {}", String::from_utf8_lossy(&nasm_result.stdout));
            eprintln!("stderr: {}", String::from_utf8_lossy(&nasm_result.stderr));
        }

        // Run "ld -o test test.o"
        let mut output_ld = Command::new("/usr/bin/ld");
        output_ld.args(&["-o", &file_stem.to_str().unwrap(), &format!("{}.o", &file_stem.to_str().unwrap())]);

        println!("Linking... {:?}", output_ld);

        let ld_result = output_ld.output()
            .expect("Failed to execute command");

        // Print output of ld command
        if !ld_result.stdout.is_empty() {
            println!("{}", String::from_utf8_lossy(&ld_result.stdout));
        }
        if !ld_result.stderr.is_empty() {
            eprintln!("{}", String::from_utf8_lossy(&ld_result.stderr));
        }
    }

    pub fn run(&mut self) {
        let run_command = Command::new(format!("{}", self.project).as_str())
            .output()
            .expect("Failed to run program");

        if !run_command.stdout.is_empty() {
            println!("{}", String::from_utf8_lossy(&run_command.stdout));
        }
        if !run_command.stderr.is_empty() {
            eprintln!("{}", String::from_utf8_lossy(&run_command.stderr));
        }
    }
}

