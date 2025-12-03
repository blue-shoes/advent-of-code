use std::fs;

fn main() {

    let filepath: &str = "inputs/day_03/input.txt";

    let seq: String = fs::read_to_string(filepath).expect("Should have read file");

    let seq: Vec<&str> = seq.split("\n").collect();

    let sum = part_one(&seq);

    println!("The maximum output joltage is {sum}");

    let sum: u64 = part_two(&seq);

    println!("The maximum output override joltage is {sum}");
    
}

fn part_one(seq: &Vec<&str>) -> u64 {
    let mut sum: u64 = 0;

    for line in seq {
        let mut max_ones: u64 = 0;
        let mut max_tens: u64 = 0;
        for val in line.chars().rev() {
            let val: u64 = val.to_digit(10).expect("Converted char to digit").into();

            if max_ones == 0 {
                max_ones = val;
                continue;
            }
            if val >= max_tens {
                if max_tens > max_ones {
                    max_ones = max_tens;
                }
                max_tens = val;
            }
        }
        sum += 10*max_tens + max_ones;
    }
    sum
}

fn part_two(seq: &Vec<&str>) -> u64 {
    let mut sum: u64 = 0;

    let pow_10: [f64; 12] = [1e11f64, 1e10f64, 1e9f64, 1e8f64, 1e7f64, 1e6f64, 1e5f64, 1e4f64, 1e3f64, 1e2f64, 1e1f64, 1e0f64];

    for line in seq {
        let mut voltage: [u64; 12] = [0; 12];
        'char_loop: for val in line.chars().rev() {
            let val: u64 = val.to_digit(10).expect("Converted char to digit").into();

            // Fill array first
            for v_idx in (0..12).rev() {
                if voltage[v_idx] == 0 {
                    voltage[v_idx] = val;
                    continue 'char_loop;
                }
            }
            //Check for new max digit
            let mut start_idx = 12;
            
            if val >= voltage[0] && voltage[0] < voltage[1] {
                start_idx = 0;
            }
            else{
                for v_idx in 0..11 {
                    if voltage[v_idx] >= voltage[v_idx+1] {
                        if v_idx == 10 {
                            start_idx = 12;
                            break;

                        }
                        else if voltage[v_idx+1] < voltage[v_idx+2] {
                            start_idx = v_idx+2;
                            break;

                        }
                    }
                }
            }

            if val >= voltage[0] {
                for v_idx in (1..start_idx).rev() {
                    voltage[v_idx] = voltage[v_idx-1];
                }
                voltage[0] = val;
            }
        }
        let volt: u64 = voltage.iter()
            .zip(pow_10.iter())
            .map(|(a, b)|a*(b.round() as u64))
            .sum();

        sum += volt;
    }

    sum
}