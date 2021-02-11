use std::vec::Vec;
use std::fmt;
use crate::chunk::value;

#[derive(Debug)]
pub enum OpCode {
    OpConstant,
    OpReturn,
}

#[derive(Debug)]
pub struct Chunk {
    code: Vec<(u32, OpCode)>,
    constants: value::ValueArray,
}

impl Chunk {
    pub fn new() -> Chunk {
        Chunk{
            code: Vec::new(),
            constants: value::ValueArray::new(),
        }
    }

    pub fn write_chunk(&mut self, byte: OpCode){
        let line_number = self.code.len()as u32  + 1;
        self.code.push((line_number, byte))
    }

    pub fn add_constant(&mut self, value: value::Value) -> usize{
        self.constants.write_value_array(value)
    }
}

impl fmt::Display for Chunk {
    // TODO: find why this overflows the stack
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut results: Vec<fmt::Result>= Vec::new();
        results.push(write!(f, "===VM INSTR===\n"));
        for opcode in self.code.iter() {
            results.push(write!(f, "{:?}", opcode));
        }

        // Check for failures
        results.iter().fold(Ok(()), |_, val| match val {
            Err(x) => Err(*x),
            _     => Ok(())
        })
    }
}
