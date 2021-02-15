use std::vec::Vec;
use std::rc::Rc;
use std::env;
use std::fmt;

use crate::chunk::chunk;
use crate::chunk::value;
use crate::vm::stack;

#[derive(Debug)]
pub struct VM {
    chunk : Rc<chunk::Chunk>,
    ip: Rc<chunk::Code>,
    instruction_index: usize,
    stack: stack::Stack<value::Value>,
}

impl VM {
    pub fn new(chunk: chunk::Chunk) -> VM{
        VM {
            ip: Rc::new(chunk.code()),
            chunk: Rc::new(chunk),
            instruction_index: 0,
            stack: stack::Stack::<value::Value>::new(512),
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
            // Debug info
            match env::var("RUST_BACKTRACE") {
                Ok(_) => {
                    println!("{}", self);
                },
                Err(_) => (),
            }
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

#[derive(Debug,PartialEq)]
pub enum InterpretResult{
    Ok,
    CompileError,
    RuntimeError,
    Continue,
}

impl fmt::Display for VM {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut results : Vec<fmt::Result> = Vec::new();
        results.push(write!(f, "=================VM================\n"));
        results.push(write!(f, "================CHUNK==============\n"));
        results.push(write!(f, "{}", *self.chunk));
        results.push(write!(f, "NEXT_INSTR: {:?}, INSTRUCTION_INDEX: {:?}", self.ip, self.instruction_index));
        results.push(write!(f, "STACK: \n {:?}", self.stack));
        crate::utils::util::fold_results(results)
    }
}
