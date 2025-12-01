use std::fs;

fn main() {

    let dial_start = 50;

    let filepath = "input.txt";

    let dial = dial_start;

    let seq = fs::read_to_string(filepath).expect("Should have read file");

    let seq: Vec<&str> = seq.split("\n").collect();

    let part1_count = part1_solution(&seq, dial);
    println!("The dial rested at zero after {part1_count} steps.");

    let dial = dial_start;
    let part2_count: i32 = part2_solution(&seq, dial);
    println!("The dial passed zero {part2_count} times.");


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

fn part2_solution(seq: &Vec<&str>, mut dial: i32) -> i32 {
    let mut count = 0;

    for step in seq {
        let dir = &step[..1];
        let clicks = &step[1..].parse::<i32>().expect("Should have parsed number of clicks");

        count += clicks / 100;

        let partial = clicks % 100;

        let orig_dial = dial;

        dial = match dir {
            "L" => dial - partial,
            "R" => dial + partial,
            _ => dial,
        };

        dial = dial % 100;
        if dial < 0 {
            dial += 100;
        }

        if orig_dial == 0 {
            continue;
        }

        if dial == 0 {
            count += 1;
        }else if dir == "L" && dial > orig_dial{
            count += 1;
        } else if dir == "R" && dial < orig_dial{
            count +=1;
        }

    }
    count
}
