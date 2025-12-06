use std::fs;

fn main() {
    let filepath = "inputs/day_06/input.txt";
    
    let seq: String = fs::read_to_string(filepath).expect("Should have read file");

    let lines: Vec<&str> = seq.split("\n").collect();

    let opers: Vec<&str> = lines[lines.len()-1].split_whitespace().collect();

    let sum: u64 = part_one(&lines, &opers);

    println!("The sum of the answers is {sum}");

    let sum: u64 = part_two(&lines, &opers);

    println!("The sum of the answers in cephalopod math is {sum}");
    
}

fn part_one(lines: &Vec<&str>, opers: &Vec<&str>) -> u64 {
    let vals: Vec<&str> = lines[0].split_whitespace().collect();

    let mut vals: Vec<u64> = vals.iter()
                                    .map(|v: &&str| v.parse::<u64>()
                                    .expect("Got int"))
                                    .collect();

    for line in &lines[1..lines.len()-1]{
        let l_vals: Vec<&str> = line.split_whitespace().collect();
        let l_vals: Vec<u64> = l_vals.iter()
                                        .map(|v: &&str| v.parse::<u64>()
                                        .expect("Got int"))
                                        .collect();

        for (idx,l_val) in l_vals.iter().enumerate(){
            match opers[idx] {
                "*" => vals[idx] = vals[idx] * l_val,
                "+" => vals[idx] = vals[idx] + l_val,
                _ => ()
            };
        }
    }

    let sum:u64 = vals.iter().sum();
    sum
}

fn part_two(lines: &Vec<&str>, opers: &Vec<&str>) -> u64 {
    let line_chars: Vec<Vec<char>> = lines.iter()
                                        .map(|l|l.chars()
                                                            .filter(|c|*c != '*' && *c != '+')
                                                            .collect::<Vec<char>>())
                                        .collect();
    let mut sum: u64 = 0;
    
    let max = &line_chars[0].len();

    let mut prob_count: usize = 0;

    let mut val: u64 = 0;

    for idx in 0..(*max) {
        let mut n = String::from("");
        for l in &line_chars[0..line_chars.len()-1] {
            n.push(l[idx]);
        }
        let n = n.trim();

        if n.is_empty() {
            sum += val;
            prob_count += 1;
            val = 0;
            continue;
        }
        let n: u64 = n.parse().expect("Got number");
        match opers[prob_count] {
            "*" => {if val == 0 {val = n} else {val = val * n}},
            "+" => val = val + n,
            _ => ()
        };        
    }   

    sum + val
}