mod chunk;
mod vm;
#[macro_use]
extern crate lazy_static;

fn main() {
    let mut chunk = chunk::chunk::Chunk::new();
    chunk.write_chunk(chunk::chunk::OpCode::Return);
    chunk.add_constant(1.2 as f64);
    // chunk.dissasemble()
    let mut vm = vm::vm::VM::new(chunk);
    vm.interpret();
}
