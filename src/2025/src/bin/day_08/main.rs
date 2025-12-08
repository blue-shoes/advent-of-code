use std::{collections::HashMap, fs};

#[derive(PartialEq)]
#[derive(Hash)]
#[derive(Eq)]
#[derive(Copy, Clone)]
#[derive(Debug)]
struct Coords{
    x: i64,
    y: i64,
    z: i64
}
impl Coords {
    fn get_dist(&self, sister: &Coords) -> u64 {
        let squared_dist: u64 = (self.x - sister.x).pow(2) as u64
                                + (self.y - sister.y).pow(2) as u64
                                + (self.z - sister.z).pow(2) as u64;
        
        return squared_dist;
    }

    
}

#[derive(Clone)]
#[derive(Debug)]

struct Circuit {
    boxes: Vec<Coords>
}

impl Circuit {
    fn combine_circuits(&mut self, circuit: &Circuit) {
        self.boxes.extend_from_slice(&circuit.boxes[..]);
    }
}

fn main() {

    

    let filepath = "inputs/day_08/input.txt";
    
    let seq: String = fs::read_to_string(filepath).expect("Should have read file");

    let lines: Vec<&str> = seq.split("\n").collect();

    let j_boxes: Vec<Coords> = lines.iter()
                                    .map(|x| get_coords(x))
                                    .collect();
    
    let mut circuit_list: Vec<Circuit> = vec![];

    let mut c_map: HashMap<Coords, usize> = HashMap::new();

    for (idx, c) in j_boxes.iter().enumerate() {
        let circ: Circuit = Circuit { boxes: vec![*c] };
        circuit_list.push(circ);
        c_map.insert(*c, idx);
    }

    let mut distances: HashMap<u64, (&Coords, &Coords)> = HashMap::new();

    for (idx, c) in j_boxes.iter().enumerate() {
        for c1 in &j_boxes[(idx+1)..] {
            distances.insert(c.get_dist(c1),(c, c1));
        } 
    }

    let mut sorted_keys: Vec<u64> = distances.keys().copied().collect();
    sorted_keys.sort();
    
    let multiple = part_one(&sorted_keys, &distances, &mut c_map, &mut circuit_list);
    println!("Multiple of three largest circuits is {multiple}");

    let prod = part_two(&sorted_keys, &distances, &mut c_map, &mut circuit_list);
    println!("Multiple of last two x coordinates is {prod}");


}

fn part_two(sorted_keys: &Vec<u64>, 
            distances: &HashMap<u64, (&Coords, &Coords)>, 
            c_map: &mut HashMap<Coords, usize>, 
            circuit_list: &mut Vec<Circuit>) 
        -> u64 {

    let pairs_to_connect = 1000;

    let mut x_prod: i64 = 0;

    for d in &sorted_keys[pairs_to_connect..] {
        let conn = distances.get(d).expect("Got distance");

        let circ_idx = c_map.get(conn.0).expect("Got circuit").clone();
        let c_circuit = &circuit_list[circ_idx];
        if c_circuit.boxes.contains(conn.1){
            continue;
        }
        
        let c2_idx = c_map.get(conn.1).expect("Got circuit 2");

        let circ2 = &circuit_list[*c2_idx].clone();

        for c in &circ2.boxes {
            c_map.insert(*c, circ_idx);
        }
        circuit_list[circ_idx].combine_circuits(circ2);

        if circuit_list[circ_idx].boxes.len() == circuit_list.len() {
            x_prod = conn.0.x * conn.1.x;
            break;
        }
    }

    x_prod as u64
}

fn part_one(sorted_keys: &Vec<u64>, 
            distances: &HashMap<u64, (&Coords, &Coords)>, 
            c_map: &mut HashMap<Coords, usize>, 
            circuit_list: &mut Vec<Circuit>)
    -> u64 {
    let pairs_to_connect = 1000;
    for d in &sorted_keys[..pairs_to_connect] {
        let conn = distances.get(d).expect("Got distance");
        let circ_idx = c_map.get(conn.0).expect("Got circuit").clone();
        let c_circuit = &circuit_list[circ_idx];
        if c_circuit.boxes.contains(conn.1){
            continue;
        }
        
        let c2_idx = c_map.get(conn.1).expect("Got circuit 2");

        let circ2 = &circuit_list[*c2_idx].clone();

        for c in &circ2.boxes {
            c_map.insert(*c, circ_idx);
        }
        circuit_list[circ_idx].combine_circuits(circ2);

    }

    let mut circuit_size_map: HashMap<usize, u64> = HashMap::new();
    for c_idx in c_map.values() {
        
        let circ = &circuit_list[*c_idx];
        circuit_size_map.insert(*c_idx, circ.boxes.len() as u64);
    }

    let mut sizes: Vec<&u64> = circuit_size_map.values().collect();
    sizes.sort();
    sizes.reverse();

    sizes[0] * sizes[1] * sizes[2]

}

fn get_coords(line: &&str) -> Coords{
    let c_vec: Vec<i64> = line.split(",")
        .into_iter()
        .map(|c| c.parse::<i64>().expect("Got coodinate."))
        .collect();
    Coords{x:c_vec[0], y:c_vec[1], z:c_vec[2]}
}