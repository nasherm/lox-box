use std::vec::Vec;
use std::fmt;
use crate::chunk::value;

#[derive(Debug, Clone, Copy)]
pub enum OpCode {
    Constant,
    Return,
    Undefined(usize),
}

pub type Code = Vec<(u32, OpCode)>;

#[derive(Debug)]
pub struct Chunk {
    current_line_number: u32,
    code: Code,
    constants: value::ValueArray,
}

impl Chunk {
    pub fn new()-> Chunk {
        Chunk{
            current_line_number: 0,
            code: Vec::new(),
            constants: value::ValueArray::new(),
        }
    }

    pub fn write_chunk(&mut self, op: OpCode){
        self.current_line_number += 1;
        self.code.push((self.current_line_number, op))
    }

    pub fn add_constant(&mut self, value: value::Value){
        let index = self.constants.write_value_array(value);
        self.write_chunk(OpCode::Constant);
        self.code.push((self.current_line_number, OpCode::Undefined(index)))
    }

    pub fn dissasemble(&self) {
        println!("{}", self)
    }

    pub fn code(&self) -> Code {
        self.code.clone()
    }

    pub fn get_value(&self, value_index: usize) -> value::Value {
        self.constants.get_value(value_index)
    }
}

impl fmt::Display for Chunk {
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
