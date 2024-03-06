use std::vec::Vec;
use std::ops::Index;

#[derive(Debug, Copy, Clone)]
enum ValueType {
    Bool,
    Nil,
    Num,
}
union ValueUnion {
    b: bool,
    f: f64,
}

#[derive(Debug, Copy, Clone)]
struct Value {
    _type: ValueType,
    _as: ValueUnion,
}

impl Value {
    pub fn bool_val(value: f64) -> Self  {
        Value {
            _type: ValueType::Bool,
            _as: ValueUnion { b: value > 0.0 }
        }
    }

    pub fn nil_val(value: f64) -> Self {
        Value {
            _type: ValueType::Nil,
            _as: ValueUnion { f: 0.0 }
        }
    }

    pub fn num_val(val: f64) -> Self {
        Value {
            _type: ValueType::Num,
            _as: ValueUnion { f: val }
        }
    }

    pub fn as_bool(&self) -> bool {
        // TODO: is there a nicer way of doing this without unsafe
        unsafe {
            self._as.b
        }
    }

    pub fn as_num(&self) -> f64 {
        unsafe {
            self._as.f
        }
    }

    pub fn is_bool(&self) -> bool { self._type == ValueType::Bool }
    pub fn is_num(&self) -> bool { self._type == ValueType::Num }
    pub fn is_nil(&self) -> bool { self._type == ValueType::Nil }
}


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
