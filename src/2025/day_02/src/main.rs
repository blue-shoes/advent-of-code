use std::fs;

fn main() {
    let filepath = "input.txt";
    
    let seq: String = fs::read_to_string(filepath).expect("Should have read file");

    let seq: Vec<&str> = seq.split(",").collect();

    let mut seq_array: Vec<(u64, u64)> = Vec::with_capacity(seq.len());

    for v in seq{
        let r: Vec<&str>= v.split("-").collect();

        let min: u64 = r[0].parse().expect("Should have parsed minimum");
        let max: u64 = r[1].parse().expect("Should have parsed minimum");

        let pair: (u64, u64) = (min, max);
        seq_array.push(pair);
    }

    let mut count = 0;
    let mut count2 = 0;

    for r in seq_array {
        for id in r.0..(r.1+1) {
            let id_str: String = id.to_string();
            let id_len = id_str.len();
            let half = id_len / 2;

            if half == 0 {
                // Single digit can't be bad id.
                continue;
            }

            for poss_chunk in (1..(half+1)).rev() {

                if id_len % poss_chunk != 0 {
                    continue;
                }
                let poss_len = id_len / poss_chunk;

                let sub_str = &id_str[..poss_chunk];
                let test_str = sub_str.repeat(poss_len);

                if test_str == id_str {
                    count2 += id;
                    if poss_len == 2 {
                        count += id;
                    }
                    break;
                }
            }

        }
    }

    println!("There sum of the bad ids was {count}.");
    println!("There sum of the bad part 2 ids was {count2}.");


}
