use std::io::{self, prelude::*, Write, BufReader};
use std::fs::File;


pub fn repl() -> io::Result<()> {
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
        interpret(&line);
    }

    Ok(())
}

fn interpret(s: &String) -> () {
    ()
}

pub fn interpret_file(s: &String) -> io::Result<()> {
    let f = File::open(s)?;
    let reader = BufReader::new(f);

    let mut source = reader.lines();
    Ok(())
}
