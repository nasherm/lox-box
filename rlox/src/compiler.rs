use crate::vm::InterpretResult;
use crate::scanner::{Scanner, TokenType, Token};
use crate::chunk::{Chunk, OpCode};

struct Parser {
    current: Token, 
    previous: Token,
    had_error: bool,
    panic_mode: bool,
}

pub struct Compiler {
    scanner: Scanner,
    parser: Parser, 
    compiling_chunk: // TODO: make this a shared pointer
}

impl Compiler {
    pub fn init(source_code: &String) -> Self {
        Compiler {
            scanner: Scanner::init(&source_code),
            parser: Parser {
                current: Token::init(), 
                previous: Token::init(),
                had_error: false,
                panic_mode: false,
            },
            compiling_chunk: Chunk::init(),
        }
    }

    pub fn interpret(&mut self) -> InterpretResult {
        let mut line = -1;
        loop {
            let token = self.scanner.scan_token();
            if token.line != line {
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

    pub fn compile(&mut self, chunk_ptr: /* TODO */) -> bool {
        self.compiling_chunk = ???;
        self.advance();
        self.expression();
        self.consume(TokenType::TOKEN_EOF, "Expect end of expression.");
        self.end_compiler();
        !self.parser.had_error
    }

    pub fn current_chunk(&self) -> Chunk {
        return self.compiling_chunk;
    }

    fn end_compiler(&mut self) -> () {
        self.emit_return();
    }

    fn emit_return(&mut self) -> () {
        self.emit_byte(OpCode::OpReturn);
    }

    fn emit_bytes(&mut self, byte1: OpCode, byte2: OpCode) -> () {
        self.emit_byte(byte1);
        self.emit_byte(byte2);
    }

    fn error_at_current(&mut self, message: &str) -> () {
        let token = &mut self.parser.current;
        self.error_at(token, message);
    } 

    fn error(&mut self, message: &str) -> () {
        let token = &mut self.parser.previous;
        self.error_at(token, message);
    }

    fn error_at(&mut self, token: &Token, message: &str) -> () {
        if self.parser.panic_mode { // Error suppression
            return
        }

        self.parser.panic_mode = true;
        eprint!("[line {} Error]", token.line);
        if token.token_type == TokenType::TOKEN_EOF {
            eprint!(" at end");
        } else if token.token_type == TokenType::TOKEN_ERROR {
            ();
        } else {
            eprint!(" at {} {}", token.length, token.start);
        }

        eprint!(": {}", message);
        self.parser.had_error = true;
    }

    fn advance(&mut self) -> () {
        self.parser.previous = self.parser.current;
        loop {
            self.parser.current = self.scanner.scan_token();
            if self.parser.current.token_type != TokenType::TOKEN_ERROR {
                break
            }
            self.error_at_current("");
        }
    }

    fn expression(&mut self) {
        // TODO
    }

    fn consume(&mut self, token_type: TokenType, message: &str) -> () {
        if self.parser.current.token_type == token_type {
            self.advance();
        }
        self.error_at_current(message);
    }

    fn emit_byte(&mut self, byte: OpCode) -> () {
        self.compiling_chunk.write_chunk(byte, self.parser.previous.line as u32)
    }
}
