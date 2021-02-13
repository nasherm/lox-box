My work done as I  read [Crafting Interpreters](https://craftinginterpreters.com/)

The Lox specification can be found in the above link or directly [here](https://craftinginterpreters.com/appendix-i.html)

This project consists of two parts

## Plox (status: complete)
This is a compiler for Lox written in Python. It leverages the Python runtime
to allow for easy development of an interpreter for Lox.
It's not highly performant as expected, and performs no optimisations.
Main features include static analysis of programs, object-orientation suppport,
and support for the whole Lox specification (OO, recursion, functions, state, ...).

### Usage
    ./plox.py <lox-script>

or use the REPL

    ./plox.py

## Rox (status: building)
This is a compiler for Lox written in Rust. Following in the 
tradition of other bytecode VMs such as the JVM, and LLVM, this leverages
the [three phase compiler model](https://www.aosabook.org/en/llvm.html). Written in Rust, it uses the features
of the development language to allow for well typed, memory safe development. 
This compiler does perform optimisations, and supports garbage collection.


