use std::{collections::{HashMap, HashSet}, fs};

struct Grid {
    height: usize,
    width: usize,
    tiles: Vec<i8>,
    x_coords: HashMap<i64, usize>,
    y_coords: HashMap<i64, usize>,
}

impl Grid {
    fn new(x_coords: std::collections::HashSet<i64>, y_coords: std::collections::HashSet<i64>) -> Grid{
        let mut x: Vec<&i64> = x_coords.iter().collect();
        x.sort();
        
        let mut x_m: HashMap<i64, usize> = HashMap::new();
        for (i, v) in x.iter().enumerate() {
            x_m.insert(**v, i);
        }

        let mut y: Vec<&i64> = y_coords.iter().collect();
        y.sort();

        let mut y_m: HashMap<i64, usize> = HashMap::new();
        for (i, v) in y.iter().enumerate() {
            y_m.insert(**v, i);
        }
        
        let hu = x.len() + 1;
        let wu = y.len() + 1;

        let t: Vec<i8> = vec![0; (hu*wu).try_into().unwrap()];

        Grid{height: hu, width: wu, tiles: t, x_coords: x_m, y_coords: y_m}
    }

    fn convert_coord(&self, c:(i64, i64)) -> (usize, usize) {
        let x_idx = self.x_coords.get(&c.0).expect("Missing x coord");
        let y_idx = self.y_coords.get(&c.1).expect("Missing y coord");
        (*x_idx, *y_idx)
    }

    fn set_tile(&mut self, c: (usize, usize), val:i8) {
        self.set_tile_u(c, val);
    }

    fn set_tile_u(&mut self, c: (usize, usize), val:i8) {
        let idx: usize = c.0*self.width + c.1; 
        self.tiles[idx] = val;
    }

    fn set_tile_line(&mut self, c1: (i64, i64), c2: (i64, i64)) {
        let c1_conv = self.convert_coord(c1);
        let c2_conv = self.convert_coord(c2);
        let mut h_span = [c1_conv.0, c2_conv.0];
        h_span.sort();

        let mut w_span = [c1_conv.1, c2_conv.1];
        w_span.sort();

        for h in h_span[0]..(h_span[1]+1) {
            for w in w_span[0]..(w_span[1]+1) {
                if (h,w) == c1_conv || (h,w) == c2_conv {
                    self.set_tile_u((h,w), 2);
                } else {
                    self.set_tile_u((h, w), 1);
                }
            }
        }
    }

    fn get_tile(&self, c: (usize, usize)) -> i8 {
        self.tiles[c.0*self.width + c.1]
    }

    fn fill_green_tiles(&mut self) {
                
        for i in 0..self.height {
            self.recursive_color((i, 0));
            self.recursive_color((i, self.width-1));
        }
        for j in 0..self.width {
            self.recursive_color((0, j));
            self.recursive_color((self.height-1, j));
        }

        for i in 0..self.height {
            for j in 0..self.width {
                if self.get_tile((i, j)) == 0 {
                    self.set_tile((i, j),1);
                }
            }
        }
    }

    fn get_next_coord(&self, c: (usize, usize), adj: (i32, i32)) -> Option<(usize, usize)>{
        if c.0 ==0 && adj.0 < 0 {
            return None;
        }
        if c.1 ==0 && adj.1 < 0 {
            return None;
        }
        if c.0 >= self.height-1  && adj.0 > 0{
            return None;
        }
        if c.1 >= self.width-1 && adj.1 > 0{
            return None
        }
        Some(((c.0 as i32 + adj.0) as usize, (c.1 as i32 + adj.1) as usize))
    }

    fn recursive_color(&mut self, c: (usize, usize)) {
        if self.get_tile(c) != 0 {
            return;
        }

        self.set_tile(c, -1);
        let neighbors: Vec<(i32, i32)> = vec![(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1,-1), (1, 0), (1, 1)];
        for adj in &neighbors {
            let next_c = self.get_next_coord(c, *adj);
            let next_c = match next_c {
                Some(next_c) => next_c,
                None => continue
            };
            if self.get_tile(next_c) == 0 {
                self.recursive_color(next_c);
            }
        }
    }

    #[allow(dead_code)]
    fn print_grid(&self) {

        for i in 0..self.height {
            for j in 0..self.width {
                let v = self.get_tile((i, j));
                if v == -1 {
                    print!(".");
                }else if v == 1 {
                    print!("X");
                } else if v == 2 {
                    print!("0");
                } else {
                    print!("!")
                }
            }
            print!("\n");
        }
    }

    fn valid_rectangle(&self, c1: &(i64, i64), c2:&(i64, i64)) -> bool {
        let mut h_span = [self.x_coords.get(&c1.0).unwrap(), self.x_coords.get(&c2.0).unwrap()];
        h_span.sort();

        let mut w_span = [self.y_coords.get(&c1.1).unwrap(), self.y_coords.get(&c2.1).unwrap()];
        w_span.sort();

        for h in *h_span[0]..(*h_span[1]+1) {
            for w in *w_span[0]..(*w_span[1]+1) {
                if self.get_tile((h, w))< 0 {
                    return false;
                }
            }
        }
        return true;
    }
}

fn main() {
    let filepath = "inputs/day_09/inputs.txt";
    
    let seq: String = fs::read_to_string(filepath).expect("Should have read file");

    let seq: Vec<&str> = seq.split("\n").collect();

    let c_list: Vec<(i64, i64)> = seq.iter()
                                        .map(|l|get_coords(l))
                                        .collect();

    let max_area = part_one(&c_list);

    println!("The largest rectangle area is {max_area}");

    let max_area = part_two(&c_list);

    println!("The largest rectangle area with only red or green tiles is {max_area}");

}

fn part_two(c_list: &Vec<(i64, i64)>) -> u64 {
    let mut max_area: u64 = 0;

    let mut h = 0;
    let mut w = 0;

    let mut y_set: std::collections::HashSet<i64> = HashSet::new();
    let mut x_set: std::collections::HashSet<i64> = HashSet::new();

    for c in c_list{
        x_set.insert(c.0);
        if c.0 > h {
            h = c.0;
        }
        y_set.insert(c.1);
        if c.1 > w {
            w = c.1;
        }
    }

    let mut grid: Grid = Grid::new(x_set, y_set);

    for (idx,c) in c_list[..c_list.len()-1].iter().enumerate() {
        grid.set_tile_line(*c, c_list[idx+1]);
    }

    // List wraps
    grid.set_tile_line(c_list[0], c_list[c_list.len()-1]);

    grid.fill_green_tiles();

    //grid.print_grid();

    for (idx, c1) in c_list.iter().enumerate() {
        for c2 in &c_list[(idx+1)..] {
            let area = get_area(c1, c2);
            if area > max_area {
                if grid.valid_rectangle(c1, c2) {
                    max_area = area;
                }
            }
        }
    }
    max_area
}

fn part_one(c_list: &Vec<(i64, i64)>) -> u64 {
    let mut max_area: u64 = 0;

    for (idx, c1) in c_list.iter().enumerate() {
        for c2 in &c_list[(idx+1)..] {
            let area = get_area(c1, c2);
            if area > max_area {
                max_area = area;
            }
        }
    }

    max_area
}

fn get_area(c1: &(i64, i64), c2: &(i64, i64)) -> u64 {
    let x: u64 = ((c1.0 - c2.0).abs() + 1).try_into().unwrap();
    let y: u64 = ((c1.1 - c2.1).abs() + 1).try_into().unwrap();

    x*y
}

fn get_coords(line: &str) -> (i64, i64) {
    let split: Vec<&str>= line.split(",").collect();
    (split[0].parse().expect("X-coord parsed."), split[1].parse().expect("Y-coord parsed."))
}