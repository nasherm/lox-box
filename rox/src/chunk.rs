use std::vec::Vec;
use std::fmt;

#[derive(Debug)]
pub enum OpCode {
    OpReturn,
}

#[derive(Debug)]
pub struct Chunk {
    code: Vec<OpCode>,
}

impl Chunk {
    pub fn new() -> Chunk {
        Chunk{
            code: Vec::new(),
        }
    }

    pub fn write_chunk(&mut self, byte: OpCode){
        self.code.push(byte);
    }
}

impl fmt::Display for Chunk {
    // TODO: find why this overflows the stack
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut results: Vec<fmt::Result>= Vec::new();
        results.push(write!(f, "===VM INSTR===\n"));
        for opcode in self.code.iter() {
            results.push(opcode.fmt(f));
        }

        // Check for failures
        results.iter().fold(Ok(()), |_, val| match val {
            Err(x) => Err(*x),
            _     => Ok(())
        })
    }
}

impl fmt::Display for OpCode {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self)
    }
}
