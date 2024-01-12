use std::io::{self, prelude::*, Write, BufReader};
use std::fs::File;
use std::ops::{Deref, DerefMut};
use crate::vm::{InterpretResult};
use crate::compiler::Compiler;
use crate::chunk::{Chunk};
use crate::vm::InterpretResult::InterpretCompilerError;
use crate::vm::Vm;


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
    let mut compiler = Compiler::init(s);
    if !(compiler.compile()) {
        return InterpretCompilerError;
    }
    match compiler.current_chunk()  {
        Ok(mut chunk) =>  {
            let mut chunk_inner = chunk.borrow_mut();
            let mut vm = Vm::init(chunk_inner.deref_mut());
            vm.run()
       },
       _ => InterpretCompilerError
    }
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
