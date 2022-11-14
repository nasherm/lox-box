mod chunk;
mod debug;
mod value;
mod vm;
mod common;

use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    let _ = match args.len() {
        1 => common::repl(),
        2 => common::interpret_file(&args[0]),
        _ => {
            println!("Usage: ./rlox <input_file>");
            Ok(())
        }
    };
}
