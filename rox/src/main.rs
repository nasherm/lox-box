mod chunk;
mod vm;
mod utils;
#[macro_use]
extern crate lazy_static;

fn main() {
    let mut chunk = chunk::chunk::Chunk::new();
    chunk.add_constant( 1.2 as f64);
    chunk.add_constant(3.4 as f64);
    chunk.write_chunk(chunk::chunk::OpCode::Add); // %1 = 1.2 + 3.4
    chunk.add_constant(5.6 as f64);
    chunk.write_chunk(chunk::chunk::OpCode::Divide); // %2 = %1 / 5.6
    chunk.write_chunk(chunk::chunk::OpCode::Negate); // %2 = - %2
    chunk.write_chunk(chunk::chunk::OpCode::Return);
    // chunk.dissasemble()
    let mut vm = vm::vm::VM::new(chunk);
    vm.interpret();
}
