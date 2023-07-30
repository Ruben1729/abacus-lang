use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

#[derive(Debug, PartialEq, Eq)]
pub enum LexicalToken {
    Keyword(String),
    Literal(String),
    Operator(String),
}

pub fn tokenize(file_path: &str) -> Vec<LexicalToken> {
    let path = Path::new(file_path);
    let file = File::open(&path).expect("Unable to open file.");
    let reader = io::BufReader::new(file);

    let mut lexical_tokens: Vec<LexicalToken> = Vec::new();

    for line in reader.lines() {
        if line.is_ok() {
            for token in line.expect("Unable to lex file.").split_whitespace() {
                match token {
                    _ if token.parse::<i32>().is_ok() => lexical_tokens.push(
                        LexicalToken::Literal(token.to_string())
                    ),
                    "pop" | "print" |
                    "dup" | "copy" | "over" |
                    "swap" |
                    "if" | "elif" | "else" |
                    "while" |
                    "end" | "do" | "endloop" =>
                        lexical_tokens.push(
                            LexicalToken::Keyword(token.to_string())),
                    "+" | "-" |
                    "==" | ">" | ">=" | "<" | "<=" => lexical_tokens.push(
                        LexicalToken::Operator(token.to_string())
                    ),
                    "//" => {
                        break;
                    },
                    _ => (),
                }
            }
        }
    }

    lexical_tokens
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lexing() {
        let tokens = tokenize("./tests/simple_addition.aba");
        assert_eq!(tokens.len(), 3);
        assert_eq!(tokens.get(0).unwrap(), &LexicalToken::Literal("2".parse().unwrap()));
        assert_eq!(tokens.get(1).unwrap(), &LexicalToken::Literal("2".parse().unwrap()));
        assert_eq!(tokens.get(2).unwrap(), &LexicalToken::Operator("+".parse().unwrap()));
    }

}
