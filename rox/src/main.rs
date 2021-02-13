mod chunk;
mod vm;
#[macro_use]
extern crate lazy_static;

fn main() {
    let mut vm = vm::vm::VM::new();

    let mut chunk = chunk::chunk::Chunk::new();
    chunk.write_chunk(chunk::chunk::OpCode::OpReturn);
}
