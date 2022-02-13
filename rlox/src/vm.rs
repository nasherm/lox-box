use crate::chunk::{Chunk, OpCode};
use crate::value::{Value, print_value};
use crate::debug;

pub enum InterpretResult{
    InterpretOk,
    InterpretCompilerError,
    InterpretRuntimeError,
}

pub struct Vm<'a>{
    chunk: &'a Chunk,
    ip: u32,
    stack: [Value; 256],
    sp: u8,
}

impl<'a> Vm<'a> {
    pub fn init(chunk: &'a mut Chunk) -> Self {
        Vm {
            chunk,
            ip: 0,
            stack: [0.0;256],
            sp: 0,
        }
    }

    pub fn push(&mut self, value: Value) -> () {
        self.stack[self.sp as usize] = value;
        self.sp += 1;
    }

    pub fn pop(&mut self) -> Value {
        self.sp -= 1;
        self.stack[self.sp as usize]
    }

    fn deref_ip(&mut self) -> OpCode {
        self.ip += 1;
        self.chunk.get_instr((self.ip - 1) as usize)
    }

    fn read_constant(&mut self) -> Value {
        self.chunk.get_constant_val(self.deref_ip())
    }

    fn binop(&mut self, f: &dyn Fn(Value, Value) -> Value){
        let v2 = self.pop();
        let v1 = self.pop();
        self.push(f(v1, v2));
    }

    pub fn run(&mut self) -> InterpretResult {
        loop {
            if cfg!(debug_assertions) {
                print!("       ");
                let mut i = 0;
                while i < self.sp {
                    print!("[ {:?} ]", self.stack[i as usize]);
                    i += 1;
                }
                println!();
                debug::disassemble_instruction(self.chunk, self.ip as usize);
            }

            match self.deref_ip() {
                OpCode::OpConstant => {
                    let val = self.read_constant();
                    self.push(val);
                },
                OpCode::OpNegate => {
                    let x = -self.pop();
                    self.push(x);
                },
                OpCode::OpAdd => self.binop(&mut |x, y| x + y),
                OpCode::OpSub => self.binop(&mut |x, y| x - y),
                OpCode::OpMult => self.binop(&mut |x, y| x * y),
                OpCode::OpDiv => self.binop(&mut |x, y| x / y),
                _ => {
                    print_value(self.pop());
                    return InterpretResult::InterpretOk
                }
            }
        }
    }

}
