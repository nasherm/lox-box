use crate::vm::InterpretResult;
use crate::scanner::{Scanner, TokenType, Token};

pub struct Compiler {
    scanner: Scanner,
}

impl Compiler {
    pub fn init(source_code: &String) -> Self {
        Compiler {
            scanner: Scanner::init(&source_code),
        }
    }

    pub fn compile(&mut self) -> InterpretResult {
        let mut line = -1;
        loop {
            let token = self.scanner.scan_token();
            if (token.line != line) {
                print!("{}", token.line);
                line = token.line;
            } else {
                print!("    | ");
            }
            let token_chars = self.scanner.token_chars(token.length);
            print!("{:?}  {:?}", token.token_type, token_chars);
            if token.token_type == TokenType::TOKEN_EOF {
                break
            }
        }
        InterpretResult::InterpretOk
    }
}
