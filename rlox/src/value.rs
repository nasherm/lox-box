use std::vec::Vec;
use std::ops::Index;

pub type Value = f64;

pub fn print_value(value: Value) -> () {
    println!("{:?}", value)
}

// Constants are stored in a value array,
// and we access said constants by being aware
// of their index
#[derive(Clone, Debug)]
pub struct ValueArray{
    values: Vec<Value>,
}

impl ValueArray {
    pub fn init() -> Self {
        ValueArray {
            values: Vec::new(),
        }
    }

    pub fn write_value(&mut self, value: Value) -> ()  {
        self.values.push(value);
    }

    pub fn count(&self) -> usize {
        self.values.len()
    }

    pub fn get_val(&self, index: usize) -> Value{
        self.values[index]
    }

}

impl Index<usize> for ValueArray {
    type Output = Value;

    fn index(&self, index: usize) -> &Self::Output {
        &self.values[index]
    }
}
