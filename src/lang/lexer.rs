use std::fs::{File, remove_file};
use std::io::{self, BufRead};
use std::path::Path;

pub fn tokenize_file<P>(filename: P) -> io::Result<Vec<String>>
    where
        P: AsRef<Path>,
{
    let file = File::open(&filename)?;
    let reader = io::BufReader::new(file);

    let mut results = Vec::new();

    for line in reader.lines() {
        let line = line?;
        let tokens: Vec<String> = line.split_whitespace().map(String::from).collect();
        results.extend(tokens);
    }

    Ok(results)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use std::fs::File;

    #[test]
    fn test_tokenize_file() {
        let result = tokenize_file("tests/vector_addition").expect("Unable to tokenize file.");
        assert_eq!(result, vec!["<1,2,3>", "+", "<3,2,1>",
                                "<4,5,2>", "+", "<1,2,5>"]);
    }
}
