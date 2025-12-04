use std::{fs};

struct Map {
    width: i32,
    height: i32,
    data: Box<[bool]>
}

impl Map {
    fn get_coord(&self, x: i32, y:i32) -> bool {
        let idx = (y*self.width + x) as usize;
        self.data[idx]
    }

    fn set_coord_false(&mut self, x: i32, y:i32) {
        let idx = (y*self.width + x) as usize;
        self.data[idx] = false;
    }
}

fn main() {
    let filepath: &str = "inputs/day_04/input.txt";

    let seq: String = fs::read_to_string(filepath).expect("Should have read file");

    let lines: Vec<&str> = seq.split("\n").collect();

    let h = lines.len();
    let w = lines[0].len();

    let mut data: Box<[bool]> = vec![false; h*w].into_boxed_slice();
    

    for (idx, line) in lines.iter().enumerate() {
        let locs:Vec<usize> = line.bytes()
            .enumerate()
            .filter(|(_, b)| *b == b'@')
            .map(|(i, _)| i)
            .collect();

        for i in locs {
            data[w*idx + i] = true;
        }
    }

    let map: Map = Map{
        width: w as i32,
        height: h as i32,
        data: data
    };

    let movable: u64 = part_one(&map);

    println!{"There are {movable} movable rolls."};

    let total_movable: i64 = part_two(map);

    println!{"There are {total_movable} movable rolls."};


}

fn part_two(mut map: Map) -> i64 {
    let mut count: i64 = 0;

    let mut last_count: i64 = -1;

    while last_count != count {
        last_count = count;
        for x in 0..map.width as i32{
            for y in 0..map.height as i32{
                if map.get_coord(x, y) {
                    let mut occupied = 0;
                    for diff_x in -1..2 as i32{
                        for diff_y in -1..2 as i32{
                            if diff_x == 0 && diff_y == 0 {
                                continue;
                            }
                            let check_x = x+diff_x;
                            if check_x < 0 || check_x == map.width{                            
                                continue;
                            }
                            let check_y = y+diff_y;
                            if check_y < 0 || check_y == map.height{
                                continue;
                            }
                            if map.get_coord(check_x, check_y){
                                occupied += 1;
                            }
                        }
                    }
                    if occupied < 4 {
                        count +=1;
                        map.set_coord_false(x, y);
                    }
                }
            }
        }

    }

    count
}

fn part_one(map: &Map) -> u64 {
    let mut count: u64 = 0;

    for x in 0..map.width as i32{
        for y in 0..map.height as i32{
            if map.get_coord(x, y) {
                let mut occupied = 0;
                for diff_x in -1..2 as i32{
                    for diff_y in -1..2 as i32{
                        if diff_x == 0 && diff_y == 0 {
                            continue;
                        }
                        let check_x = x+diff_x;
                        if check_x < 0 || check_x == map.width{                            
                            continue;
                        }
                        let check_y = y+diff_y;
                        if check_y < 0 || check_y == map.height{
                            continue;
                        }
                        if map.get_coord(check_x, check_y){
                            occupied += 1;
                        }
                    }
                }
                if occupied < 4 {
                    count +=1;
                }
            }
        }
    }

    count
}