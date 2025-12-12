use std::fs;

#[derive(Debug)]
struct Tree {
    width: u32,
    height: u32,
    presents: Vec<u32>
}

fn main() {
    let filepath = "inputs/day_12/inputs.txt";
    
    let seq: String = fs::read_to_string(filepath).expect("Should have read file");

    let lines: Vec<&str> = seq.split("\n").collect();

    let mut presents: Vec<Vec<bool>> = Vec::new();
    let mut trees: Vec<Tree> = Vec::new();

    for (idx, line) in lines.iter().enumerate() {
        if line.contains("x") {
            trees.push(parse_tree(line));
        } else if line.contains(":") {
            presents.push(parse_present(&lines, idx));
        }
    }

    let num_fit = part_one(trees);
    println!("There are {num_fit} trees that can fit their presents.");
}

fn part_one(trees: Vec<Tree>) -> u64 {
    let mut work: u64 = 0;
    for tree in &trees {
        let area = tree.width * tree.height;
        let required:u32 = tree.presents.iter()
                                    .map(|p|p*9)
                                    .sum();
        if required <= area {
            println!("{tree:?}");
            work += 1;
        }
    }
    work
}

fn parse_tree(line: &str) -> Tree {
    let s1: Vec<&str> = line.split(":").collect();
    println!("{}", s1[0]);
    let size: Vec<u32> = s1[0].split("x")
                                .map(|v| v.parse().expect("Got size dimensions"))
                                .collect();
    
    let presents: Vec<u32> = s1[1].trim().split_whitespace()
                                        .map(|v| v.parse().expect("Got present number."))
                                        .collect();

    Tree {height: size[0], width: size[1], presents:presents}
}

fn parse_present(lines: &Vec<&str>, start_idx:usize) -> Vec<bool> {
    let mut present = Vec::new();
    for i in 1..4 {
        let line = lines[start_idx+i].chars();
        for c in line {
            present.push(c=='#');
        }
    }
    present

}