use std::vec::Vec;

use crate::chunk::chunk;

pub struct VM {
    chunk : chunk::Chunk,
    ip: chunk::Code,
}

impl VM {
    pub fn new() -> VM{
        VM {
            chunk: chunk::Chunk::new(),
            ip: Vec::new(),
        }
    }

    pub fn interpret(&mut self, chunk: chunk::Chunk) -> InterpretResult {
        self.ip = chunk.code();
        self.chunk = chunk;
        self.run()
    }

    fn run(&self) -> InterpretResult {
        InterpretResult::InterpretOk
    }
}


pub enum InterpretResult{
    InterpretOk,
    InterpretCompileError,
    InterpretRuntimeError,
}
