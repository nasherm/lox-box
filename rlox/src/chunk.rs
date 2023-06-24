use std::vec::Vec;
use crate::value::{ValueArray, Value};

#[derive(Debug, Clone, Copy)]
#[repr(u8)]
pub enum OpCode{
    Byte(u8),
    OpConstant,
    OpReturn,
    OpNegate,
    OpAdd,
    OpSub,
    OpMult,
    OpDiv,
}

// Chunks define our bytecode to execute in a
// VM. This wraps a certain state within the context
// of execution
#[derive(Clone)]
pub struct Chunk {
    code: Vec<OpCode>,
    value_array: ValueArray,
    lines: Vec<u32>,
}

impl Chunk {
    pub fn init() -> Self {
        Chunk{
            code: Vec::new(),
            value_array: ValueArray::init(),
            lines: Vec::new(),
        }
    }

    pub fn write_chunk(&mut self, op: OpCode, line: u32) -> () {
        self.code.push(op);
        self.lines.push(line);
    }

    pub fn count(&self) -> usize {
        self.code.len()
    }

    pub fn get_instr(&self, offset: usize) -> OpCode {
        return self.code[offset]
    }

    pub fn add_constant(&mut self, value: Value) -> usize{
        self.value_array.write_value(value);
        return self.value_array.count() - 1;
    }

    pub fn get_constant_val(&self, opcode: OpCode) -> Value {
        let index: u8 = match opcode {
            OpCode::Byte(x) => x,
            _ => {
                // Trigger exception
                assert_eq!(true, false);
                0xff
            }
        };
        self.value_array.get_val(index as usize)
    }

    pub fn get_line(&self, offset: usize) -> u32 {
        self.lines[offset]
    }
}
