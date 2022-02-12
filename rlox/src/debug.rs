use crate::chunk::{OpCode, Chunk};
use std::string::String;

pub fn disassemble_chunk(chunk: &Chunk, name: String) -> () {
    println!(" == {} ==", name);
    let code_count = chunk.count();
    let mut i = 0;
    while i < code_count{
        i = disassemble_instruction(chunk, i);
    }
}

fn print_constant(chunk: &Chunk, instr: OpCode, offset: usize) -> usize {
    let constant = chunk.get_constant_val(chunk.get_instr(offset + 1));
    println!("{:?} {:?}", instr, constant);
    offset + 2
}

pub fn disassemble_instruction(chunk: &Chunk, offset: usize) -> usize {
    print!("{:#010x}:\t", offset);
    // Print line information
    if offset > 0  && chunk.get_line(offset) == chunk.get_line(offset - 1){
        print!("  | ");
    } else {
        print!("{} ", chunk.get_line(offset));
    }

    // Print instruction
    let mut instruction = chunk.get_instr(offset);
    match instruction{
        OpCode::OpConstant  => print_constant(chunk, instruction, offset),
        _ => {
            println!("{:?}", instruction);
            offset + 1
        }
    }
}

