use std::fs;

fn main() {
    let filepath = "inputs/day_05/input.txt";
    
    let seq: String = fs::read_to_string(filepath).expect("Should have read file");

    let seq: Vec<&str> = seq.split("\n").collect();

    let mut seq_array: Vec<(u64, u64)> = Vec::with_capacity(seq.len());

    let mut ranges: bool = true;

    let mut fresh_count: u64 = 0;

    for v in seq{
        if v.is_empty() {
            ranges = false;
            continue;
        }
        if ranges {
            let r: Vec<&str>= v.split("-").collect();

            let min: u64 = r[0].parse().expect("Should have parsed minimum");
            let max: u64 = r[1].parse().expect("Should have parsed minimum");

            let pair: (u64, u64) = (min, max);
            seq_array.push(pair);
        } else {
            let ingred:u64 = v.parse().expect("Should have parsed ingredient");
            for r in &seq_array {
                if ingred >= r.0 && ingred <= r.1 {
                    fresh_count +=1;
                    break;
                }
            }
        }
    }

    println!("There are {fresh_count} fresh ingredient IDs.");

    let total_fresh_ids = part_two(seq_array);

    println!("There are {total_fresh_ids} total fresh ingredient IDs.");

}

fn part_two(mut seq_array: Vec<(u64,u64)>) -> u64 {
    let mut count = 0;

    seq_array.sort();

    let mut last_id = 0;

    for r in &seq_array {
        let mut start = r.0;
        if r.1 <= last_id {
            continue;
        }
        if r.0 <= last_id {
            start = last_id+1;
        }
        count += r.1 - start + 1;
        last_id = r.1;
    }

    count
}