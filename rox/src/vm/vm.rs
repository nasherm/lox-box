use std::vec::Vec;
use std::rc::Rc;
use std::env;
use std::fmt;
use std::option::Option;
use std::string::String;

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
                (_, chunk::OpCode::Negate)   => self.handle_negate(),
                (_, chunk::OpCode::Constant) => self.handle_constant(),
                (_, chunk::OpCode::Add)      => self.handle_binop(&|x, y| x + y),
                (_, chunk::OpCode::Subtract) => self.handle_binop(&|x, y| x - y),
                (_, chunk::OpCode::Multiply) => self.handle_binop(&|x, y| x*y),
                (_, chunk::OpCode::Divide)   => self.handle_binop(&|x, y| x/y),
                (_, chunk::OpCode::Return)   => self.handle_return(),
                _ => InterpretResult::RuntimeError(None),
            }
        }
        status
    }

    fn push(&mut self, value: value::Value) -> Result<(), ()> {
        self.stack.push(value)
    }

    fn pop(&mut self) -> Option<value::Value>{
        self.stack.pop()
    }

    fn handle_negate(&mut self) -> InterpretResult {
        match self.pop() {
            Some(x) => {
                let result = self.push( -x);
                if result.is_err() {
                    return InterpretResult::RuntimeError(Some(String::from("Failure push negative to stack")))
                }
                InterpretResult::Continue
            },
            _ => InterpretResult::RuntimeError(Some(String::from("Failure popping from empty stack"))),
        }
    }

    fn handle_constant(&mut self) -> InterpretResult {
        match self.read_byte() {
            (_, chunk::OpCode::Undefined(x)) =>
            {
                let value = self.chunk.get_value(x);
                if self.push(value).is_err(){
                    return InterpretResult::RuntimeError(Some(String::from("Failure pushing constant to stack")));
                }
                InterpretResult::Continue
            },
            _ => InterpretResult::RuntimeError(Some(String::from("No value associated with constant: FATAL"))),
        }
    }

    fn handle_return(&mut self) -> InterpretResult {
        match self.pop() {
            Some(x) => println!("{}", x),
            _ => (),
        };
        InterpretResult::Continue
    }

    fn handle_binop(&mut self, func: &dyn Fn(value::Value, value::Value) -> value::Value) -> InterpretResult {
        let y = self.pop();
        let x = self.pop();
        let result = match (x, y) {
            (Some(x), Some(y)) => self.push(func(x, y)),
            _ => Err(()),
        };
        if result.is_err() {
            return InterpretResult::RuntimeError(Some(String::from("Failed to push result of binop")))
        }
        InterpretResult::Continue
    }
}

#[derive(Debug,PartialEq)]
pub enum InterpretResult{
    Ok,
    CompileError,
    RuntimeError(Option<String>),
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
