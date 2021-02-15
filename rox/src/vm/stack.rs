use std::vec::Vec;

#[derive(Debug)]
pub struct Stack<T> {
    max_size: usize,
    items: Vec<T>,
}

impl <T> Stack<T> {
    pub fn new(max_size: usize) -> Stack<T> {
        Stack {
            max_size,
            items: Vec::with_capacity(max_size),
        }
    }

    pub fn pop(&mut self) -> Option<T> {
        self.items.pop()
    }

    pub fn push(&mut self, item: T) -> Result<(), ()> {
        match self.items.len() == self.max_size {
            true => Err(()),
            false =>{
                self.items.push(item);
                Ok(())
            }
        }
    }

    pub fn size(&self) -> usize {
        self.items.len()
    }

    pub fn peek(&self) -> Option<&T> {
        self.items.last()
    }
}
