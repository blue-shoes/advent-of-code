use std::fs;

fn main() {

    let dial_start = 50;

    let filepath = "input.txt";

    let dial = dial_start;

    let seq = fs::read_to_string(filepath).expect("Should have read file");

    let seq: Vec<&str> = seq.split("\n").collect();

    let part1_count = part1_solution(&seq, dial);
    println!("The dial rested at zero after {part1_count} steps.");

}

fn part1_solution(seq: &Vec<&str>, mut dial: i32) -> i32 {
    let mut part1_count = 0;

    for step in seq {
        let dir = &step[..1];
        let clicks = &step[1..].parse::<i32>().expect("Should have parsed number of clicks");
        
        dial = match dir {
            "L" => dial - clicks,
            "R" => dial + clicks,
            _ => dial,
        };

        if dial % 100 == 0 {
            part1_count += 1;
        }
    }

    part1_count
}
