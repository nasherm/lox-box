use std::ops::Deref;
use crate::vm::InterpretResult;
use crate::scanner::{Scanner, TokenType, Token};
use crate::chunk::{Chunk, OpCode};
use std::{rc::Rc, cell::RefCell};

struct Parser {
    current: Token, 
    previous: Token,
    had_error: bool,
    panic_mode: bool,
}

pub struct Compiler {
    scanner: Scanner,
    parser: Parser, 
    compiling_chunk: Rc<RefCell<Chunk>>,// TODO: make this a shared pointer
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
            compiling_chunk: Rc::new(RefCell::new(Chunk::init())),
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

    pub fn compile(&mut self) -> bool {
        self.compiling_chunk = Rc::new(RefCell::new(Chunk::init()));
        self.advance();
        self.expression();
        self.consume(TokenType::TOKEN_EOF, "Expect end of expression.");
        self.end_compiler();
        !self.parser.had_error
    }

    pub fn current_chunk(&self) -> Result<RefCell<Chunk>, Rc<RefCell<Chunk>>> {
        Rc::try_unwrap(self.compiling_chunk.to_owned())
    }

    fn end_compiler(&mut self) -> () {
        self.emit_return();
    }

    fn emit_return(&mut self) -> () {
        self.emit_byte(OpCode::OpReturn);
    }

    fn error_at_current(&mut self, message: &str) -> () {
        self.error_at(self.parser.current.clone(), message);
    } 

    fn error(&mut self, message: &str) -> () {
        self.error_at(self.parser.previous.clone(), message);
    }

    fn error_at(&mut self, token: Token, message: &str) -> () {
        if self.parser.panic_mode { // Error suppression
            return
        }

        self.parser.panic_mode = true;
        eprint!("[line {} Error]", token.line);
        match token.token_type {
            TokenType::TOKEN_EOF => eprint!(" at end"),
            TokenType::TOKEN_ERROR => (),
            _ => eprint!(" at {} {}", token.length, token.start),
        };
        eprint!(": {}", message);
        self.parser.had_error = true;
    }

    fn advance(&mut self) -> () {
        self.parser.previous = self.parser.current.clone();
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
        self.compiling_chunk.borrow_mut().write_chunk(byte, self.parser.previous.line as u32)
    }

    fn emit_bytes(&mut self, byte1: OpCode, byte2: OpCode) -> () {
        self.emit_byte(byte1);
        self.emit_byte(byte2);
    }
}
