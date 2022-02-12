mod chunk;
mod debug;
mod value;
fn main() {
    let mut chunk = chunk::Chunk::init();
    let constant = chunk.add_constant(1.2);
    chunk.write_chunk(chunk::OpCode::OpConstant, 123);
    chunk.write_chunk(chunk::OpCode::Byte(constant as u8), 123);
    chunk.write_chunk(chunk::OpCode::OpReturn, 123);
    debug::disassemble_chunk(&chunk, String::from("My Chunk"));
}
