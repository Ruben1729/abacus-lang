use crate::parser::Instruction;

pub struct Simulator {
    stack: Vec<i32>
}

impl Simulator {
    pub fn new() -> Self {
        Simulator {
            stack: Vec::new()
        }
    }

    pub fn start(&mut self, mut instructions: Vec<Instruction>) {
        while instructions.len() > 0 {
            if let Some(instruction) = instructions.pop() {
                match instruction {
                    Instruction::Pop => {
                        self.stack.pop();
                    }
                    Instruction::Push(val) => {
                        self.stack.push(val.parse::<i32>().expect("Unknown type"));
                    }
                    Instruction::Print => {
                        if let Some(val) = self.stack.last() {
                            println!("{}", val);
                        }
                    }
                    Instruction::Add => {
                        let val1 = self.stack.pop().expect("Not enough arguments in the stack.");
                        let val2 = self.stack.pop().expect("Not enough arguments in the stack.");

                        self.stack.push(val1 + val2);
                    }
                    Instruction::Sub => {
                        let val1 = self.stack.pop().expect("Not enough arguments in the stack.");
                        let val2 = self.stack.pop().expect("Not enough arguments in the stack.");

                        self.stack.push(val1 - val2);
                    }
                }
            }
        }
    }
}
