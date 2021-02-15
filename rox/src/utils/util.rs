use std::fmt;
use std::vec::Vec;

pub fn fold_results(results: Vec<fmt::Result>) -> fmt::Result {
    results.iter().fold(Ok(()), |_, val| match val {
        Err(x) => Err(*x),
        _     => Ok(())
    })
}
