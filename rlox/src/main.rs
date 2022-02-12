mod chunk;
mod debug;
mod value;
mod vm;

fn main() {
    let mut chunk = chunk::Chunk::init();
    let constant = chunk.add_constant(1.2);
    chunk.write_chunk(chunk::OpCode::OpConstant, 123);
    chunk.write_chunk(chunk::OpCode::Byte(constant as u8), 123);
    chunk.write_chunk(chunk::OpCode::OpNegate, 123);
    chunk.write_chunk(chunk::OpCode::OpReturn, 123);
    debug::disassemble_chunk(&chunk, String::from("My Chunk"));
    let mut vm = vm::Vm::init(&mut chunk);
    vm.run();
}
