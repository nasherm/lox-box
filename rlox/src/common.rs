use std::io::{self, prelude::*, Write, BufReader};
use std::fs::File;
use crate::vm::{InterpretResult};
use crate::compiler;


pub fn repl() -> Result<(), InterpretResult> {
    let mut line: String = String::new();
    let stdin = io::stdin();

    loop {
        print!(">");
        io::stdout().flush();
        stdin.read_line(&mut line);
        line.pop(); // Remove new line
        if line == "q" {
            break
        };
        match interpret(&line) {
            InterpretResult::InterpretOk=> (),
            result => return Err(result),
        };
    }

    Ok(())
}

fn interpret(s: &String) -> InterpretResult {
    let compiler = compiler::Compiler::init(s);
    compiler.compile()
}

pub fn interpret_file(s: &String) -> Result<(), InterpretResult> {
    let f = File::open(s).unwrap();
    let reader = BufReader::new(f);
    let mut source = reader.lines().fold(String::new(), |acc, line| acc + &line.unwrap());
    match interpret(&source) {
        InterpretResult::InterpretOk => Ok(()),
        result => Err(result),
    }
}
