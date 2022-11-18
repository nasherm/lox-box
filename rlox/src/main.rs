mod chunk;
mod debug;
mod value;
mod vm;
mod common;
mod compiler;
mod scanner;

use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    let _ = match args.len() {
        1 => common::repl(),
        2 => match common::interpret_file(&args[1]) {
            Ok(()) => Ok(()),
            Err(err) =>{
                println!("Interpreting failed, ERROR: {:?}", err);
                Err(err)
            }
        }
        _ => {
            println!("Usage: ./rlox [input_file]");
            Ok(())
        }
    };
}
