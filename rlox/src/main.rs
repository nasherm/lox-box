mod chunk;
mod debug;
mod value;
mod vm;

fn main() {
    let mut chunk = chunk::Chunk::init();
    let mut constant = chunk.add_constant(1.2);
    chunk.write_chunk(chunk::OpCode::OpConstant, 123);
    chunk.write_chunk(chunk::OpCode::Byte(constant as u8), 123);
    chunk.write_chunk(chunk::OpCode::OpNegate, 123);
    constant = chunk.add_constant(3.4);
    chunk.write_chunk(chunk::OpCode::OpConstant, 123);
    chunk.write_chunk(chunk::OpCode::Byte(constant as u8), 123);
    chunk.write_chunk(chunk::OpCode::OpAdd, 123);
    constant = chunk.add_constant(5.6);
    chunk.write_chunk(chunk::OpCode::OpConstant, 123);
    chunk.write_chunk(chunk::OpCode::Byte(constant as u8), 123);
    chunk.write_chunk(chunk::OpCode::OpDiv, 123);
    chunk.write_chunk(chunk::OpCode::OpReturn, 123);
    debug::disassemble_chunk(&chunk, String::from("My Chunk"));
    let mut vm = vm::Vm::init(&mut chunk);
    vm.run();
}
