use std::fs;

fn main() {
    let filepath = "inputs/day_07/input.txt";
    
    let seq: String = fs::read_to_string(filepath).expect("Should have read file");

    let lines: Vec<&str> = seq.split("\n").collect();

    let split_count: u64 = part_one(&lines);

    println!("The tachyon beam was split {split_count} times.");

    let timeline_count: u64 = part_two(&lines);

    println!("The tachyon beam has {timeline_count} timeline.");

}

fn part_one(lines: &Vec<&str>)-> u64 {
    let mut beams: Vec<bool> = lines[0].chars()
                                        .into_iter()
                                        .map(|c| c == 'S')
                                        .collect();
    
    let mut split_count: u64 = 0;

    for line in &lines[1..] {
        let mut next_line: Vec<bool> = vec!(false; line.len());

        let line_chars: std::str::Chars<'_> = line.chars();

        for (idx, (beam, s_char)) in beams.iter().zip(line_chars).enumerate() {
            if !beam {
                continue;
            }
            match s_char {
                '.' => next_line[idx] = true,
                '^' => {
                        if idx > 0 {next_line[idx-1] = true;} 
                        if idx < line.len()-1 {next_line[idx+1] = true;} 
                        split_count += 1
                    },
                _ => ()
            }
        }
        beams = next_line;

    }

    split_count
}

fn part_two(lines: &Vec<&str>) -> u64 {
    let mut beams: Vec<u64> = lines[0].chars()
                                    .into_iter()
                                    .map(|c| if c == 'S' {1} else {0})
                                    .collect();

    for line in &lines[1..] {
        let mut next_line: Vec<u64> = vec!(0; line.len());

        let line_chars: std::str::Chars<'_> = line.chars();

        for (idx, (beam, s_char)) in beams.iter().zip(line_chars).enumerate() {
            if *beam == 0u64 {
                continue;
            }
            match s_char {
                '.' => next_line[idx] += *beam,
                '^' => {
                        if idx > 0 {next_line[idx-1] += beam;} 
                        if idx < (line.len()-1) {next_line[idx+1] += beam;} 
                    },
                _ => ()
            }
        }
        beams = next_line;

    }

    beams.iter().sum() 
}