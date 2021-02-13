use std::vec::Vec;
use std::rc::Rc;

use crate::chunk::chunk;

pub struct VM {
    chunk : Rc<chunk::Chunk>,
    ip: Rc<chunk::Code>,
    instruction_index: usize,
}

impl VM {
    pub fn new(chunk: chunk::Chunk) -> VM{
        VM {
            ip: Rc::new(chunk.code()),
            chunk: Rc::new(chunk),
            instruction_index: 0,
        }
    }

    fn read_byte(&mut self) -> (u32, chunk::OpCode) {
        self.instruction_index += 1;
        self.ip[self.instruction_index - 1]
    }

    // Triggers instruction execution
    pub fn interpret(&mut self) -> InterpretResult {
        let mut status = InterpretResult::Continue;
        let mut instruction;
        while (status == InterpretResult::Continue) && (self.instruction_index < self.ip.len()){
            instruction = self.read_byte();
            status = match instruction {
                (_, chunk::OpCode::Constant) =>
                {
                    match self.read_byte() {
                        (_, chunk::OpCode::Undefined(x)) =>
                        {
                            let value = self.chunk.get_value(x);
                            println!("{:?}", value);
                            InterpretResult::Continue
                        },
                        _ => InterpretResult::RuntimeError,
                    }
                },

                (_, chunk::OpCode::Return) => InterpretResult::Continue,
                _ => InterpretResult::RuntimeError,
            }
        }
        status
    }
}

#[derive(PartialEq)]
pub enum InterpretResult{
    Ok,
    CompileError,
    RuntimeError,
    Continue,
}
