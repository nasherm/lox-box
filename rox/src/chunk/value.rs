use std::vec::Vec;


pub type Value = f64;

#[derive(Debug)]
pub struct ValueArray {
    values: Vec<Value>,
}

impl ValueArray {
    pub fn new() -> ValueArray {
        ValueArray{
            values: Vec::new(),
        }
    }

    pub fn write_value_array(&mut self, value: Value) -> usize {
        self.values.push(value);
        self.values.len() - 1
    }
}
