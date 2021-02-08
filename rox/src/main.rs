mod chunk;

fn main() {
    let mut chunk = chunk::Chunk::new();
    println!("Built chunk!");
    chunk.write_chunk(chunk::OpCode::OpReturn);
    println!("Wrote an opcode");
    println!("{:?}", chunk)
}
