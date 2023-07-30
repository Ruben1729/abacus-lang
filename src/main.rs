extern crate core;

use std::env;

pub mod compiler;
pub mod lexer;
pub mod parser;

use self::compiler::*;
use self::lexer::*;
use self::parser::*;

fn main() {
    let args: Vec<String> = env::args().collect();

    let tokens = tokenize(args.get(1).expect("Unable to get file name"));
    let instructions = parse_tokens(tokens);
    let mut compiler = Compiler::new(args.get(1).expect("Unable to get file name"));
    compiler.init();
    compiler.generate_assembly(instructions);
    // compiler.compile();
    // compiler.run();
}
