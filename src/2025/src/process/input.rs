use std::fs

fn read_input(filepath: str) {
    let seq: String = fs::read_to_string(filepath).expect("Should have read file");
}